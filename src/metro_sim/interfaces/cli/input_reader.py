import msvcrt

def key_pressed() -> str | None:
    if msvcrt.kbhit():
        return msvcrt.getwch().lower()
    return None

def read_key() -> str | None:
    if msvcrt.kbhit():
        return msvcrt.getwch().lower()
    return None


def read_blocking_key(valid_keys: set[str]) -> str:
    while True:
        key = msvcrt.getwch().lower()
        if key in valid_keys:
            return key
        
def read_valid_key(valid_keys: set[str]) -> str:
    while True:
        key = msvcrt.getwch().lower()

        if key in valid_keys:
            return key