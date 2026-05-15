from metro_sim.core.game_session import create_game_session
from metro_sim.pvp.services.station_pressure_pvp_service import influence_station_pressure


def test_player_can_influence_station_pressure():
    session = create_game_session()
    station = session.world.stations["paveletskaya"]

    before = station.pressure["sabotage"]

    result = influence_station_pressure(
        session=session,
        source_player_id="player_001",
        station_id="paveletskaya",
        pressure_key="sabotage",
        amount=5,
    )

    assert result.success is True
    assert station.pressure["sabotage"] == before + 5
    assert len(session.world.pvp_impacts) == 1


def test_station_pressure_pvp_has_cooldown():
    session = create_game_session()

    first = influence_station_pressure(
        session=session,
        source_player_id="player_001",
        station_id="paveletskaya",
        pressure_key="sabotage",
        amount=5,
    )

    second = influence_station_pressure(
        session=session,
        source_player_id="player_001",
        station_id="paveletskaya",
        pressure_key="sabotage",
        amount=5,
    )

    assert first.success is True
    assert second.success is False
    assert second.message == "pvp_action_on_cooldown"