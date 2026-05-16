from metro_sim.core.game_session import create_game_session
from metro_sim.core.game_summary_service import build_game_summary


def test_game_summary_contains_core_sections():
    session = create_game_session()

    summary = build_game_summary(session)

    assert "tick" in summary
    assert "players" in summary
    assert "stations" in summary
    assert "routes" in summary
    assert "factions" in summary
    assert "events" in summary


def test_game_summary_contains_loaded_stations():
    session = create_game_session()

    summary = build_game_summary(session)

    assert len(summary["stations"]) == len(session.world.stations)

    for station_id in session.world.stations:
        assert station_id in summary["stations"]

def test_game_summary_contains_split_paveletskaya_nodes():
    session = create_game_session()

    summary = build_game_summary(session)

    assert "paveletskaya_ring" in summary["stations"]
    assert "paveletskaya_radial" in summary["stations"]