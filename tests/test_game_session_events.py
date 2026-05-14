from metro_sim.core.game_session import advance_tick, create_game_session


def test_game_session_last_report_contains_generated_world_events():
    session = create_game_session()
    station = session.world.stations["paveletskaya"]
    station.pressure["militia_support"] = 25

    advance_tick(session)

    assert session.last_report is not None
    assert len(session.last_report.events) >= 1
    assert session.last_report.events[0].event_type == "militia_gains_control"