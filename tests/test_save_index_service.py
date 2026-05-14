from metro_sim.core.game_session import create_game_session
from metro_sim.persistence.save_game_service import save_game_session
from metro_sim.persistence.save_index_service import list_save_games


def test_list_save_games_contains_saved_game():
    session = create_game_session()

    save_game_session(session, "test_index")

    saves = list_save_games()
    save_names = {save["save_name"] for save in saves}

    assert "test_index" in save_names