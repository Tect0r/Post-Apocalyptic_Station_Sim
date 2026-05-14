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


def test_game_summary_contains_three_stations():
    session = create_game_session()

    summary = build_game_summary(session)

    assert len(summary["stations"]) == 3
    assert "paveletskaya" in summary["stations"]
    assert "polis" in summary["stations"]
    assert "hansa_ring" in summary["stations"]