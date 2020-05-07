from ps2_analysis.infantry_weapons.ammo import Ammo


def test_shots_per_clip():
    ammo: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        block_auto=None,
        continuous=None,
        short_reload_time=0,
        reload_chamber_time=0,
        loop_start_time=None,
        loop_end_time=None,
        can_chamber_in_ads=None,
    )

    assert ammo.shots_per_clip == 10

    ammo.ammo_per_shot = 2

    assert ammo.shots_per_clip == 5


def test_long_reload_time():
    ammo: Ammo = Ammo(
        clip_size=5,
        total_capacity=100,
        ammo_per_shot=1,
        block_auto=None,
        continuous=None,
        short_reload_time=100,
        reload_chamber_time=10,
        loop_start_time=None,
        loop_end_time=None,
        can_chamber_in_ads=None,
    )

    assert ammo.long_reload_time == 110

    ammo.loop_start_time = 5
    ammo.loop_end_time = 10

    assert ammo.long_reload_time == 525
