def ask_until_valid(valid_inputs: set[str], prompt: str = "> ") -> str:
    while True:
        user_input = input(prompt).strip().lower()

        if user_input in valid_inputs:
            return user_input

        print("Ungültige Eingabe.")