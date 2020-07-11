from ps2_analysis.fire_groups.ammo import Ammo


def test_shots_per_clip():
    ammo: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=0,
        reload_chamber_time=0,
    )

    assert ammo.shots_per_clip == 10

    ammo: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=2,
        short_reload_time=0,
        reload_chamber_time=0,
    )

    assert ammo.shots_per_clip == 5


def test_long_reload_time():
    ammo: Ammo = Ammo(
        clip_size=5,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=100,
        reload_chamber_time=10,
    )

    assert ammo.long_reload_time == 110

    ammo: Ammo = Ammo(
        clip_size=5,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=100,
        reload_chamber_time=10,
        loop_start_time=5,
        loop_end_time=10,
    )

    assert ammo.long_reload_time == 525
