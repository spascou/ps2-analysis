import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from ps2_census.enums import FireModeType, PlayerState

from .ammo import Ammo
from .cone_of_fire import ConeOfFire
from .damage_profile import DamageProfile
from .fire_timing import FireTiming
from .heat import Heat
from .projectile import Projectile
from .recoil import Recoil

srandom = random.SystemRandom()


@dataclass
class FireMode:
    # Basic information
    type: FireModeType
    description: str
    is_ads: bool
    detect_range: float

    # Movement modifiers
    move_multiplier: float
    turn_multiplier: float

    # Damage profiles
    direct_damage_profile: Optional[DamageProfile]
    indirect_damage_profile: Optional[DamageProfile]

    # Zoom
    zoom: float

    # Sway
    sway_can_steady: Optional[bool]
    sway_amplitude_x: Optional[float]
    sway_amplitude_y: Optional[float]
    sway_period_x: Optional[float]
    sway_period_y: Optional[float]

    # Ammo
    ammo: Optional[Ammo]

    # Heat
    heat: Optional[Heat]

    # Fire timing
    fire_timing: FireTiming

    # Recoil
    recoil: Recoil

    # Projectile
    projectile: Optional[Projectile]

    # Player state cones of fire
    player_state_cone_of_fire: Dict[PlayerState, ConeOfFire]

    # Player state can ads
    player_state_can_ads: Dict[PlayerState, bool]

    @property
    def max_consecutive_shots(self) -> int:

        max_consecutive_shots: int

        if self.heat:

            max_consecutive_shots = self.heat.shots_before_overheat

        elif self.ammo:

            max_consecutive_shots = self.ammo.shots_per_clip

        else:

            raise ValueError("No Ammo nor Heat available")

        return max_consecutive_shots

    @property
    def reload_time(self) -> int:

        reload_time: int

        if self.heat:

            reload_time = self.heat.recovery_time(
                heat=self.max_consecutive_shots * self.heat.heat_per_shot
            )

        elif self.ammo:

            reload_time = self.ammo.long_reload_time

        else:

            raise ValueError("No Ammo nor Heat available")

        return reload_time

    def generate_real_shot_timings(self, shots=int) -> List[Tuple[int, bool]]:

        shot_timings: List[Tuple[int, bool]] = []

        remainder: int = shots - self.max_consecutive_shots
        reloads: int = 0

        if remainder == 0:

            shot_timings = self.fire_timing.generate_shot_timings(shots=shots)

        else:

            while True:

                if remainder < 0:

                    shot_timings += [
                        (t + reloads * self.reload_time, b)
                        for t, b in self.fire_timing.generate_shot_timings(shots=shots)
                    ]

                    break

                else:

                    shot_timings += [
                        (t + reloads * self.reload_time, b)
                        for t, b in self.fire_timing.generate_shot_timings(
                            shots=self.max_consecutive_shots
                        )
                    ]

                    reloads += 1

                remainder -= self.max_consecutive_shots

        return shot_timings

    # def simulate_shots(
    #     self, shots: int, player_state: PlayerState = PlayerState.STANDING,
    # ) -> List[Tuple[int, Tuple[float, float], List[Tuple[float, float]]]]:

    #     # Result as a list of time, cursor position tuple and pellets positions tuples
    #     result: List[Tuple[int, Tuple[float, float], List[Tuple[float, float]]]] = []

    #     # Cone of fire at player state
    #     cof: ConeOfFire = self.player_state_cone_of_fire[player_state]

    #     # Recoil
    #     recoil: Recoil = self.recoil

    #     # Fire timing
    #     fire_timing: FireTiming = self.fire_timing
    #     shot_timings: List[Tuple[int, bool]] = self.generate_real_shot_timings(
    #         shots=shots
    #     )

    #     # Damage profiles
    #     direct_damage_profile: DamageProfile = self.direct_damage_profile

    #     # Current state
    #     # Position; start at origin
    #     curr_x = 0.0
    #     curr_y = 0.0

    #     # Recoil parameters
    #     curr_max_vertical_recoil: float = recoil.max_vertical
    #     curr_min_vertical_recoil: float = recoil.min_vertical
    #     curr_max_horizontal_recoil: float = recoil.max_horizontal
    #     curr_min_horizontal_recoil: float = recoil.min_horizontal

    #     # CoF parameters
    #     curr_cof_angle: float = cof.min_angle * cof.multiplier

    #     # Loop
    #     previous_t: int = 0

    #     t: int
    #     b: bool
    #     for t, b in shot_timings:
    #         delta = t - previous_t

    #         # After first shot, apply scaling and recoveries
    #         if t > 0:

    #             # CoF scaling
    #             cof_recovery_delay: int = fire_timing.refire_time + cof.recovery_delay
    #             min_cof_angle: float = cof.min_angle * cof.multiplier
    #             max_cof_angle: float = cof.max_angle * cof.multiplier

    #             # Under recovery delay -- bloom CoF
    #             if delta <= cof_recovery_delay:
    #                 if curr_cof_angle < max_cof_angle:
    #                     curr_cof_angle += cof.bloom
    #                     curr_cof_angle = min(curr_cof_angle, max_cof_angle)

    #             # Above recovery delay -- recover CoF
    #             else:
    #                 curr_cof_angle -= (cof.recovery_rate / 1_000) * (
    #                     delta - cof_recovery_delay
    #                 )
    #                 curr_cof_angle = max(curr_cof_angle, min_cof_angle)

    #             # Recoil scaling
    #             recoil_recovery_delay: int = fire_timing.refire_time + recoil.recovery_delay
    #             full_recoil_recovery_delay: int = recoil_recovery_delay + int(
    #                 math.ceil(
    #                     math.sqrt(curr_x ** 2 + curr_y ** 2)
    #                     / (recoil.recovery_rate / 1_000)
    #                 )
    #             )

    #             # Under recovery delay -- scale recoil
    #             if delta <= recoil_recovery_delay:
    #                 # Vertical
    #                 if recoil.vertical_increase > 0:
    #                     if curr_min_vertical_recoil < curr_max_vertical_recoil:
    #                         curr_min_vertical_recoil += recoil.vertical_increase
    #                         curr_min_vertical_recoil = min(
    #                             curr_min_vertical_recoil, curr_max_vertical_recoil
    #                         )

    #                 elif recoil.vertical_increase < 0:
    #                     if curr_max_vertical_recoil > curr_min_vertical_recoil:
    #                         curr_max_vertical_recoil += recoil.vertical_increase
    #                         curr_max_vertical_recoil = max(
    #                             curr_min_vertical_recoil, curr_max_vertical_recoil
    #                         )

    #                 # Min horizontal
    #                 if recoil.min_horizontal_increase < 0:
    #                     if curr_min_horizontal_recoil > 0:
    #                         curr_min_horizontal_recoil += recoil.min_horizontal_increase
    #                         curr_min_horizontal_recoil = max(
    #                             0, curr_min_horizontal_recoil
    #                         )

    #                 elif recoil.min_horizontal_increase > 0:
    #                     if curr_min_horizontal_recoil < curr_max_horizontal_recoil:
    #                         curr_min_horizontal_recoil += recoil.min_horizontal_increase
    #                         curr_min_horizontal_recoil = min(
    #                             curr_min_horizontal_recoil, curr_max_horizontal_recoil
    #                         )

    #                 # Max horizontal
    #                 if recoil.max_horizontal_increase > 0:
    #                     curr_max_horizontal_recoil += recoil.max_horizontal_increase

    #                 elif recoil.max_horizontal_increase < 0:
    #                     if curr_max_horizontal_recoil > curr_min_horizontal_recoil:
    #                         curr_max_horizontal_recoil += recoil.max_horizontal_increase
    #                         curr_max_horizontal_recoil = max(
    #                             curr_min_horizontal_recoil, curr_max_horizontal_recoil
    #                         )

    #             # Above recovery delay but below full recovery -- recover recoil
    #             elif delta <= full_recoil_recovery_delay:
    #                 curr_x -= (
    #                     (delta - recoil_recovery_delay)
    #                     * (recoil.recovery_rate / 1_000)
    #                     * math.sin(math.atan(curr_x / curr_y))
    #                 )
    #                 curr_y -= (
    #                     (delta - recoil_recovery_delay)
    #                     * (recoil.recovery_rate / 1_000)
    #                     * math.cos(math.atan(curr_x / curr_y))
    #                 )

    #             # Above full recovery -- recenter to initial position
    #             else:
    #                 curr_x = 0
    #                 curr_y = 0

    #         # Current result
    #         curr_result: Tuple[int, Tuple[float, float], List[Tuple[float, float]]] = (
    #             t,  # time
    #             (curr_x, curr_y),  # cursor
    #             [],  # pellets
    #         )

    #         # CoF simulation
    #         cof_h: float
    #         cof_v: float
    #         cof_angle: float
    #         cof_orientation: float

    #         if curr_cof_angle == 0.0:
    #             cof_h = 0.0
    #             cof_v = 0.0
    #         else:
    #             cof_angle = srandom.uniform(0, curr_cof_angle)
    #             cof_orientation = srandom.uniform(0, 360)

    #             cof_h = cof_angle * math.cos(math.radians(cof_orientation))
    #             cof_v = cof_angle * math.sin(math.radians(cof_orientation))

    #         # Individual pellets position
    #         for _ in range(direct_damage_profile.pellets_count):

    #             pellet_h: float
    #             pellet_v: float
    #             pellet_angle: float
    #             pellet_orientation: float

    #             if cof.pellet_spread:
    #                 pellet_angle = srandom.uniform(0, cof.pellet_spread)
    #                 pellet_orientation = srandom.uniform(0, 360)

    #                 pellet_h = pellet_angle * math.cos(math.radians(pellet_orientation))
    #                 pellet_v = pellet_angle * math.sin(math.radians(pellet_orientation))

    #                 curr_result[2].append(
    #                     (curr_x + cof_h + pellet_h, curr_y + cof_v + pellet_v)
    #                 )

    #             else:
    #                 curr_result[2].append((curr_x + cof_h, curr_y + cof_v))

    #         # Un-angled vertical recoil amplitude
    #         recoil_v: float

    #         if curr_max_vertical_recoil == curr_min_vertical_recoil:
    #             recoil_v = curr_max_vertical_recoil
    #         else:
    #             recoil_v = srandom.uniform(
    #                 curr_min_vertical_recoil, curr_max_vertical_recoil
    #             )

    #         # FSM scaling of un-angled vertical recoil
    #         if b is True:
    #             recoil_v *= recoil.first_shot_multiplier

    #         # Un-angled horizontal recoil amplitude
    #         recoil_h: float

    #         if curr_max_horizontal_recoil == curr_min_horizontal_recoil:
    #             recoil_h = curr_max_horizontal_recoil
    #         else:
    #             recoil_h = srandom.uniform(
    #                 curr_min_horizontal_recoil, curr_max_horizontal_recoil
    #             )

    #         # Horizontal recoil direction
    #         recoil_h_direction: Literal[-1, 1]
    #         recoil_h_choices: Tuple[Literal[-1, 1], Literal[-1, 1]] = (-1, 1)

    #         if recoil.half_horizontal_tolerance:
    #             if abs(curr_x) <= recoil.half_horizontal_tolerance:
    #                 recoil_h_direction = srandom.choice(recoil_h_choices)
    #             else:
    #                 if curr_x > 0:
    #                     recoil_h_direction = -1
    #                 else:
    #                     recoil_h_direction = 1
    #         else:
    #             recoil_h_direction = srandom.choice(recoil_h_choices)

    #         recoil_h *= recoil_h_direction

    #         # Recoil angle
    #         recoil_a: float

    #         if (recoil.max_angle, recoil.min_angle) == (0.0, 0.0):
    #             recoil_a = 0.0
    #         elif recoil.max_angle == recoil.min_angle:
    #             recoil_a = recoil.max_angle
    #         else:
    #             recoil_a = srandom.uniform(recoil.min_angle, recoil.max_angle)

    #         # Angle horizontal and vertical recoil
    #         recoil_h_angled: float
    #         recoil_v_angled: float

    #         if recoil_a == 0.0:
    #             recoil_h_angled = recoil_h
    #             recoil_v_angled = recoil_v
    #         else:
    #             recoil_h_angled = recoil_h * math.cos(
    #                 math.radians(recoil_a)
    #             ) + recoil_v * math.sin(math.radians(recoil_a))
    #             recoil_v_angled = -recoil_h * math.sin(
    #                 math.radians(recoil_a)
    #             ) + recoil_v * math.cos(math.radians(recoil_a))

    #         # Append result
    #         result.append(curr_result)

    #         # Update current position
    #         curr_x += recoil_h_angled
    #         curr_y += recoil_v_angled

    #         previous_t = t

    #     return result
