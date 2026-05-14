from metro_sim.core.game_session import GameSession, create_game_session
from metro_sim.persistence.load_game_service import load_game_session
from metro_sim.persistence.save_game_service import save_game_session


DEFAULT_SAVE_NAME = "api_dev_save"

_game_session: GameSession | None = None


def get_game_session() -> GameSession:
    global _game_session

    if _game_session is None:
        try:
            _game_session = load_game_session(DEFAULT_SAVE_NAME)
        except FileNotFoundError:
            _game_session = create_game_session()
            save_game_session(_game_session, DEFAULT_SAVE_NAME)

    return _game_session


def replace_game_session(session: GameSession) -> None:
    global _game_session
    _game_session = session


def save_current_game_session(save_name: str = DEFAULT_SAVE_NAME) -> None:
    save_game_session(get_game_session(), save_name)


def load_game_session_into_memory(save_name: str = DEFAULT_SAVE_NAME) -> GameSession:
    session = load_game_session(save_name)
    replace_game_session(session)
    return session


def reset_game_session() -> GameSession:
    session = create_game_session()
    replace_game_session(session)
    return session