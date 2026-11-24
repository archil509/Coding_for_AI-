def search4letters(phrase: str, letters: str) -> set:
    """Return the letters from 'letters' found in the phrase."""
    found = set()

    for letter in letters:
        if letter in phrase:
            found.add(letter)

    return found
