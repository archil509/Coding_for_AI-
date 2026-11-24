def search4letters(phrase: str, letters: str) -> set:
    """Return the letters from 'letters' found in the phrase."""
    found = set()

    for letter in letters:
        if letter in phrase:
            found.add(letter)

    return found


def another_function():
    return True

message = (
    "This is a very long line that is intentionally written this way "
    "to demonstrate the E501 PEP 8 error."
)
