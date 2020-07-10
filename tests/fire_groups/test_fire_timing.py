from ps2_analysis.fire_groups.fire_timing import FireTiming


def test_total_delay():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=0,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )
    assert ft.total_delay == 0

    ft.delay = 100
    assert ft.total_delay == 100

    ft.delay = 0
    ft.charge_up_time = 200
    assert ft.total_delay == 200

    ft.delay = 100
    ft.charge_up_time = 200
    assert ft.total_delay == 300


def test_spooling_refire_time():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=100,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )
    assert ft.spooling_refire_time(0) == 100
    assert ft.spooling_refire_time(1000) == 100

    ft.refire_time = 90
    ft.spool_up_time = 1000
    ft.spool_up_initial_refire_time = 10
    assert ft.spooling_refire_time(0) == 10
    assert ft.spooling_refire_time(500) == 10
    assert ft.spooling_refire_time(1000) == 90
    assert ft.spooling_refire_time(2000) == 90


def test_generate_shot_timings():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=100,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )

    assert list(ft.generate_shot_timings(shots=3)) == [
        (0, True),
        (100, False),
        (200, False),
    ]

    assert list(
        ft.generate_shot_timings(shots=9, auto_burst_length=3, control_time=100)
    ) == [
        (0, True),
        (100, False),
        (200, False),
        (400, True),
        (500, False),
        (600, False),
        (800, True),
        (900, False),
        (1000, False),
    ]

    ft.is_automatic = False
    assert list(ft.generate_shot_timings(shots=3)) == [
        (0, True),
        (100, True),
        (200, True),
    ]

    ft.burst_length = 3
    ft.burst_refire_time = 50

    assert list(ft.generate_shot_timings(shots=6)) == [
        (0, True),
        (50, False),
        (100, False),
        (200, True),
        (250, False),
        (300, False),
    ]

    assert list(ft.generate_shot_timings(shots=6, control_time=10)) == [
        (0, True),
        (50, False),
        (100, False),
        (210, True),
        (260, False),
        (310, False),
    ]


def test_time_to_fire_shots():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=100,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )
    assert ft.time_to_fire_shots(1) == 0
    assert ft.time_to_fire_shots(2) == 100
    assert ft.time_to_fire_shots(10) == 900

    ft.delay = 50
    ft.charge_up_time = 25
    assert ft.time_to_fire_shots(1) == 75
    assert ft.time_to_fire_shots(2) == 175
    assert ft.time_to_fire_shots(10) == 975

    ft.delay = 0
    ft.charge_up_time = 0
    ft.chamber_time = 200
    assert ft.time_to_fire_shots(1) == 0
    assert ft.time_to_fire_shots(2) == 300
    assert ft.time_to_fire_shots(10) == 2700

    ft.delay = 50
    ft.charge_up_time = 25
    ft.chamber_time = 200
    assert ft.time_to_fire_shots(1) == 75
    assert ft.time_to_fire_shots(2) == 375
    assert ft.time_to_fire_shots(10) == 2775

    ft.delay = 0
    ft.charge_up_time = 0
    ft.chamber_time = 0
    ft.refire_time = 200
    ft.burst_length = 3
    ft.burst_refire_time = 100
    assert ft.time_to_fire_shots(1) == 0
    assert ft.time_to_fire_shots(2) == 100
    assert ft.time_to_fire_shots(3) == 200
    assert ft.time_to_fire_shots(4) == 400
    assert ft.time_to_fire_shots(5) == 500
    assert ft.time_to_fire_shots(6) == 600
    assert ft.time_to_fire_shots(7) == 800

    ft.delay = 50
    assert ft.time_to_fire_shots(1) == 50
    assert ft.time_to_fire_shots(2) == 150
    assert ft.time_to_fire_shots(3) == 250
    assert ft.time_to_fire_shots(4) == 500
    assert ft.time_to_fire_shots(5) == 600
    assert ft.time_to_fire_shots(6) == 700
    assert ft.time_to_fire_shots(7) == 950
