from logic_utils import (
    check_guess,
    get_hint,
    get_range_for_difficulty,
    parse_guess,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Bug: the hints used to point the wrong way ---

def test_too_high_tells_player_to_go_lower():
    # Guessing above the secret must send the player DOWN
    assert "LOWER" in get_hint("Too High")

def test_too_low_tells_player_to_go_higher():
    # Guessing below the secret must send the player UP
    assert "HIGHER" in get_hint("Too Low")


# --- Bug: the secret was cast to a string on even-numbered turns, so
# --- comparisons ran alphabetically ("9" > "80") instead of numerically.

def test_single_digit_guess_below_two_digit_secret():
    # Alphabetically "9" > "80", but 9 < 80. This must be "Too Low".
    assert check_guess(9, 80) == "Too Low"

def test_two_digit_guess_above_single_digit_secret():
    # Alphabetically "10" < "9", but 10 > 9. This must be "Too High".
    assert check_guess(10, 9) == "Too High"


# --- Boundaries ---

def test_guess_one_below_secret():
    assert check_guess(49, 50) == "Too Low"

def test_guess_one_above_secret():
    assert check_guess(51, 50) == "Too High"


# --- parse_guess ---

def test_parse_plain_number():
    assert parse_guess("42") == (True, 42, None)

def test_parse_rejects_empty_string():
    ok, value, error = parse_guess("")
    assert ok is False
    assert value is None
    assert error

def test_parse_rejects_non_numeric():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error

def test_parse_handles_none():
    ok, value, error = parse_guess(None)
    assert ok is False


# --- Bug: New Game ignored difficulty and always rolled 1-100 ---

def test_easy_range_is_narrower_than_normal():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Nonsense") == (1, 100)
