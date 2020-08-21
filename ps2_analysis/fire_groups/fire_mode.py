import functools
import math
import random
import statistics
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Literal, Optional, Tuple

import methodtools
from ps2_census.enums import FireModeType, PlayerState

from ps2_analysis.enums import DamageLocation, DamageTargetType
from ps2_analysis.geometry_utils import planetman_hit_location, random_point_in_disk
from ps2_analysis.utils import cached_tan, fastround, float_range, resolve_health_pool

from .ammo import Ammo
from .cone_of_fire import ConeOfFire
from .damage_profile import DamageProfile
from .fire_timing import FireTiming
from .heat import Heat
from .lock_on import LockOn
from .projectile import Projectile
from .recoil import Recoil


@dataclass
class FireMode:
    fire_mode_id: int
    fire_mode_type: FireModeType
    description: str
    is_ads: bool
    detect_range: float
    move_multiplier: float
    turn_multiplier: float
    zoom: float
    fire_timing: FireTiming
    recoil: Recoil
    player_state_cone_of_fire: Dict[PlayerState, ConeOfFire] = field(
        default_factory=dict
    )
    player_state_can_ads: Dict[PlayerState, bool] = field(default_factory=dict)
    projectile: Optional[Projectile] = None
    lock_on: Optional[LockOn] = None
    direct_damage_profile: Optional[DamageProfile] = None
    indirect_damage_profile: Optional[DamageProfile] = None
    sway_can_steady: Optional[bool] = None
    sway_amplitude_x: Optional[float] = None
    sway_amplitude_y: Optional[float] = None
    sway_period_x: Optional[float] = None
    sway_period_y: Optional[float] = None
    ammo: Optional[Ammo] = None
    heat: Optional[Heat] = None

    @functools.cached_property
    def max_consecutive_shots(self) -> int:

        if self.heat:

            return self.heat.shots_before_overheat

        elif self.ammo:

            return self.ammo.shots_per_clip

        else:

            return -1

    @functools.cached_property
    def reload_time(self) -> int:

        if self.heat:

            if self.max_consecutive_shots >= 0:

                return self.heat.recovery_time(
                    heat=self.max_consecutive_shots * self.heat.heat_per_shot
                )

            else:

                return -1

        elif self.ammo:

            return self.ammo.long_reload_time

        else:

            return -1

    @methodtools.lru_cache()
    def damage_per_pellet(
        self,
        distance: float,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        direct_damage: int = 0

        if self.direct_damage_profile:

            direct_damage = self.direct_damage_profile.damage_per_pellet(
                distance=distance,
                damage_target_type=damage_target_type,
                damage_location=damage_location,
            )

        indirect_damage: int = 0

        if self.indirect_damage_profile:

            indirect_damage = self.indirect_damage_profile.damage_per_pellet(
                distance=0,
                damage_target_type=damage_target_type,
                damage_location=damage_location,
            )

        return direct_damage + indirect_damage

    @methodtools.lru_cache()
    def damage_per_shot(
        self,
        distance: float,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        direct_damage: int = 0

        if self.direct_damage_profile:

            direct_damage = self.direct_damage_profile.damage_per_shot(
                distance=distance,
                damage_target_type=damage_target_type,
                damage_location=damage_location,
            )

        indirect_damage: int = 0

        if self.indirect_damage_profile:

            indirect_damage = self.indirect_damage_profile.damage_per_shot(
                distance=0,
                damage_target_type=damage_target_type,
                damage_location=damage_location,
            )

        return direct_damage + indirect_damage

    @methodtools.lru_cache()
    def shots_to_kill(
        self,
        distance: float,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        dps: int = self.damage_per_shot(
            distance=distance,
            damage_target_type=damage_target_type,
            damage_location=damage_location,
        )

        if dps > 0:

            return int(
                math.ceil(
                    resolve_health_pool(damage_target_type=damage_target_type) / dps
                )
            )

        return -1

    def shots_to_kill_ranges(
        self,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
        step: float = 0.1,
        precision_decimals: int = 2,
    ) -> Iterator[Tuple[float, int]]:

        if self.direct_damage_profile:

            if self.direct_damage_profile.damage_range_delta > 0:

                previous_stk: Optional[int] = None

                for r in float_range(
                    0.0,
                    self.direct_damage_profile.min_damage_range + step,
                    step,
                    precision_decimals,
                ):

                    stk: int = self.shots_to_kill(
                        distance=r,
                        damage_target_type=damage_target_type,
                        damage_location=damage_location,
                    )

                    if previous_stk is None or stk != previous_stk:

                        if r >= step:

                            yield (fastround(r - step, precision_decimals), stk)

                        else:

                            yield (r, stk)

                    previous_stk = stk

            else:

                yield (
                    0.0,
                    self.shots_to_kill(
                        distance=self.direct_damage_profile.max_damage_range,
                        damage_target_type=damage_target_type,
                        damage_location=damage_location,
                    ),
                )

        elif self.indirect_damage_profile:

            yield (
                0.0,
                self.shots_to_kill(
                    distance=0.0,
                    damage_target_type=damage_target_type,
                    damage_location=damage_location,
                ),
            )

    def generate_real_shot_timings(
        self,
        shots: int = -1,
        control_time: int = 0,
        auto_burst_length: Optional[int] = None,
    ) -> Iterator[Tuple[int, bool]]:

        if shots == 0:

            yield (0, False)

            return

        reloads: int = 0
        remaining: int = shots

        last_timing: Tuple[int, bool] = (0, False)

        shot_timings: List[Tuple[int, bool]]

        while shots == -1 or remaining > 0:

            if shots > 0 and remaining < self.max_consecutive_shots:

                shot_timings = [
                    (last_timing[0] + t + (reloads * self.reload_time), b)
                    for t, b in self.fire_timing.generate_shot_timings(
                        shots=remaining,
                        control_time=control_time,
                        auto_burst_length=auto_burst_length,
                    )
                ]

                remaining = 0

            else:

                shot_timings = [
                    (last_timing[0] + t + (reloads * self.reload_time), b)
                    for t, b in self.fire_timing.generate_shot_timings(
                        shots=self.max_consecutive_shots,
                        control_time=control_time,
                        auto_burst_length=auto_burst_length,
                    )
                ]

                reloads += 1

                remaining -= self.max_consecutive_shots

            yield from shot_timings

            last_timing = shot_timings[-1]

    def simulate_shots(
        self,
        shots: int = -1,
        control_time: int = 0,
        auto_burst_length: Optional[int] = None,
        player_state: PlayerState = PlayerState.STANDING,
        recoil_compensation: bool = False,
        recoil_compensation_accuracy: float = 0.0,
        precision_decimals: int = 6,
    ) -> Iterator[
        Tuple[
            int,  # time
            Tuple[float, float],  # cursor position
            List[Tuple[float, float]],  # pellets positions
            float,  # current CoF
            Tuple[float, float],  # current min and max vertical recoil
            Tuple[float, float],  # current min and max horizontal recoil
        ],
    ]:

        if shots == 0:

            yield (0, (0, 0), [], 0, (0, 0), (0, 0))

            return

        # Cone of fire at player state
        cof: ConeOfFire = self.player_state_cone_of_fire[player_state]

        # Current state
        # Position; start at origin
        curr_x = 0.0
        curr_y = 0.0

        # Recoil parameters
        curr_max_vertical_recoil: float = self.recoil.max_vertical
        curr_min_vertical_recoil: float = self.recoil.min_vertical
        curr_max_horizontal_recoil: float = self.recoil.max_horizontal
        curr_min_horizontal_recoil: float = self.recoil.min_horizontal

        # CoF parameters
        curr_cof_angle: float = cof.min_cof_angle()

        # Loop
        previous_t: int = 0

        t: int
        b: bool
        for t, b in self.generate_real_shot_timings(
            shots=shots, control_time=control_time, auto_burst_length=auto_burst_length
        ):

            delta: int = t - previous_t

            # Scaling and recoveries
            ############################################################################

            # After first shot, apply scaling and recoveries
            if t > 0:

                # CoF
                ########################################################################

                cof_recovery_delay: int = self.fire_timing.refire_time + cof.recovery_delay

                # Under recovery delay -- bloom CoF
                if delta <= cof_recovery_delay:

                    curr_cof_angle = cof.apply_bloom(current=curr_cof_angle)

                # Above recovery delay -- recover CoF
                else:

                    curr_cof_angle = cof.recover(
                        current=curr_cof_angle, time=delta - cof_recovery_delay,
                    )

                # Recoil
                ########################################################################

                recoil_recovery_delay: int = self.fire_timing.refire_time + self.recoil.recovery_delay

                # Under recovery delay -- scale recoil
                if delta <= recoil_recovery_delay:

                    # Vertical
                    (
                        curr_min_vertical_recoil,
                        curr_max_vertical_recoil,
                    ) = self.recoil.scale_vertical(
                        current_min=curr_min_vertical_recoil,
                        current_max=curr_max_vertical_recoil,
                    )

                    # Horizontal
                    (
                        curr_min_horizontal_recoil,
                        curr_max_horizontal_recoil,
                    ) = self.recoil.scale_horizontal(
                        current_min=curr_min_horizontal_recoil,
                        current_max=curr_max_horizontal_recoil,
                    )

                # Above recovery delay and have a recovery rate -- recover recoil
                else:

                    curr_x, curr_y = self.recoil.recover(
                        current_x=curr_x,
                        current_y=curr_y,
                        time=delta - recoil_recovery_delay,
                    )

            # Recoil compensation
            ############################################################################
            if recoil_compensation is True:

                if curr_y != 0.0:

                    recenter_a: float

                    if self.recoil.min_angle == self.recoil.max_angle:
                        recenter_a = self.recoil.min_angle
                    else:
                        recenter_a = (self.recoil.min_angle + self.recoil.max_angle) / 2

                    if recenter_a != 0.0:
                        curr_x -= curr_y / (cached_tan(math.radians(90 - recenter_a)))

                        if recoil_compensation_accuracy > 0.0:
                            curr_x += random.uniform(
                                -recoil_compensation_accuracy,
                                recoil_compensation_accuracy,
                            )

                    curr_y = 0.0

                    if recoil_compensation_accuracy > 0.0:
                        curr_y += random.uniform(
                            -recoil_compensation_accuracy, recoil_compensation_accuracy
                        )

            # Current result
            ############################################################################

            # Result as a tuple of time, cursor position tuple and pellets positions tuples
            curr_result: Tuple[
                int,
                Tuple[float, float],
                List[Tuple[float, float]],
                float,
                Tuple[float, float],
                Tuple[float, float],
            ] = (
                t,  # time
                (curr_x, curr_y),  # cursor
                [],  # pellets
                curr_cof_angle,  # current cof angle
                (
                    curr_min_vertical_recoil,
                    curr_max_vertical_recoil,
                ),  # current vertical recoil
                (
                    curr_min_horizontal_recoil,
                    curr_max_horizontal_recoil,
                ),  # current horizontal recoil
            )

            # CoF simulation
            ############################################################################

            cof_h: float
            cof_v: float

            if curr_cof_angle == 0.0:

                cof_h = 0.0
                cof_v = 0.0

            else:

                cof_h, cof_v = random_point_in_disk(radius=curr_cof_angle)

            # Individual pellets position
            for _ in range(
                self.direct_damage_profile.pellets_count
                if self.direct_damage_profile is not None
                else self.indirect_damage_profile.pellets_count
                if self.indirect_damage_profile is not None
                else 1
            ):

                pellet_h: float
                pellet_v: float

                if cof.pellet_spread:

                    pellet_h, pellet_v = random_point_in_disk(radius=cof.pellet_spread)

                    curr_result[2].append(
                        (
                            fastround(curr_x + cof_h + pellet_h, precision_decimals),
                            fastround(curr_y + cof_v + pellet_v, precision_decimals),
                        )
                    )

                else:

                    curr_result[2].append(
                        (
                            fastround(curr_x + cof_h, precision_decimals),
                            fastround(curr_y + cof_v, precision_decimals),
                        )
                    )

            # Recoil simulation
            ############################################################################

            # Un-angled vertical recoil amplitude
            recoil_v: float

            if curr_max_vertical_recoil == curr_min_vertical_recoil:

                recoil_v = curr_max_vertical_recoil

            else:

                recoil_v = random.uniform(
                    curr_min_vertical_recoil, curr_max_vertical_recoil
                )

            # FSM scaling of un-angled vertical recoil
            if b is True:

                recoil_v = recoil_v * self.recoil.first_shot_multiplier

            # Un-angled horizontal recoil amplitude
            recoil_h: float

            if curr_max_horizontal_recoil == curr_min_horizontal_recoil:

                recoil_h = curr_max_horizontal_recoil

            else:

                recoil_h = random.uniform(
                    curr_min_horizontal_recoil, curr_max_horizontal_recoil
                )

            # Recoil angle
            recoil_a: float

            if (self.recoil.max_angle, self.recoil.min_angle) == (0.0, 0.0):

                recoil_a = 0.0

            elif self.recoil.max_angle == self.recoil.min_angle:

                recoil_a = self.recoil.max_angle

            else:

                recoil_a = random.uniform(self.recoil.min_angle, self.recoil.max_angle)

            # Horizontal recoil direction
            recoil_h_direction: Literal[-1, 1]
            recoil_h_choices: Tuple[Literal[-1, 1], Literal[-1, 1]] = (-1, 1)

            if self.recoil.half_horizontal_tolerance:

                rta: float = cached_tan(math.radians(90 - recoil_a))

                left_bound: float = (
                    (curr_y - self.recoil.half_horizontal_tolerance) / rta
                ) if recoil_a != 0.0 else -self.recoil.half_horizontal_tolerance

                right_bound: float = (
                    (curr_y + self.recoil.half_horizontal_tolerance) / rta
                ) if recoil_a != 0.0 else self.recoil.half_horizontal_tolerance

                if left_bound <= curr_x <= right_bound:

                    recoil_h_direction = random.choice(recoil_h_choices)

                else:

                    if curr_x > right_bound:

                        recoil_h_direction = -1

                    else:

                        recoil_h_direction = 1

            else:

                recoil_h_direction = random.choice(recoil_h_choices)

            recoil_h *= recoil_h_direction

            # Angle horizontal and vertical recoil
            recoil_h_angled: float
            recoil_v_angled: float

            if recoil_a == 0.0:

                recoil_h_angled = recoil_h
                recoil_v_angled = recoil_v

            else:

                recoil_a_radians: float = math.radians(recoil_a)
                sin_recoil_a_radians: float = math.sin(recoil_a_radians)
                cos_recoil_a_radians: float = math.cos(recoil_a_radians)

                recoil_h_angled = (
                    recoil_h * cos_recoil_a_radians + recoil_v * sin_recoil_a_radians
                )

                recoil_v_angled = (
                    -recoil_h * sin_recoil_a_radians + recoil_v * cos_recoil_a_radians
                )

            # Yield
            yield curr_result

            # Update current position
            curr_x = fastround(curr_x + recoil_h_angled, precision_decimals)
            curr_y = fastround(curr_y + recoil_v_angled, precision_decimals)

            previous_t = t

    def damage_inflicted_by_pellets(
        self,
        distance: float,
        pellets: List[Tuple[float, float]],
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        aim_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        damage: int = 0

        pellet_h_angle: float
        pellet_v_angle: float

        for pellet_h_angle, pellet_v_angle in pellets:

            pellet_x: float = cached_tan(math.radians(pellet_h_angle)) * distance
            pellet_y: float = cached_tan(math.radians(pellet_v_angle)) * distance

            hit_location: Optional[DamageLocation] = planetman_hit_location(
                x=pellet_x, y=pellet_y, aim_location=aim_location
            )

            damage += (
                self.damage_per_pellet(
                    distance=distance,
                    damage_target_type=damage_target_type,
                    damage_location=hit_location,
                )
                if hit_location
                else 0
            )

        return damage

    def real_time_to_kill(
        self,
        distance: float = 1.0,
        runs: int = 1,
        max_time: int = 20_000,
        control_time: int = 0,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        auto_burst_length: Optional[int] = None,
        aim_location: DamageLocation = DamageLocation.TORSO,
        player_state: PlayerState = PlayerState.STANDING,
        recoil_compensation: bool = False,
        recoil_compensation_accuracy: float = 0.0,
        precision_decimals: int = 6,
    ) -> Tuple[int, float]:

        if not self.direct_damage_profile and not self.indirect_damage_profile:

            return (-1, 1.0)

        ttks: List[int] = []

        dtk: int = resolve_health_pool(damage_target_type=damage_target_type)

        if dtk == -1:

            return (-1, 1.0)

        timed_out_simulations: int = 0

        simulation: Iterator[
            Tuple[
                int,
                Tuple[float, float],
                List[Tuple[float, float]],
                float,
                Tuple[float, float],
                Tuple[float, float],
            ]
        ]
        for simulation in (
            self.simulate_shots(
                shots=-1,
                control_time=control_time,
                auto_burst_length=auto_burst_length,
                player_state=player_state,
                recoil_compensation=recoil_compensation,
                recoil_compensation_accuracy=recoil_compensation_accuracy,
                precision_decimals=precision_decimals,
            )
            for _ in range(runs)
        ):

            total_damage: int = 0

            t: int
            pellets_coors: List[Tuple[float, float]]
            for t, _, pellets_coors, _, _, _ in simulation:

                if t > max_time:

                    timed_out_simulations += 1

                    break

                total_damage += self.damage_inflicted_by_pellets(
                    distance=distance,
                    pellets=pellets_coors,
                    damage_target_type=damage_target_type,
                    aim_location=aim_location,
                )

                if total_damage >= dtk:

                    ttks.append(t)

                    break

        if ttks:

            quantiles: List[float] = statistics.quantiles(
                ttks, n=20, method="inclusive"
            )

            return (
                int(
                    math.ceil(
                        statistics.mean(
                            filter(lambda x: quantiles[1] <= x <= quantiles[-1], ttks)
                        )
                    )
                ),
                (timed_out_simulations / runs),
            )

        else:

            return (-1, 1.0)
