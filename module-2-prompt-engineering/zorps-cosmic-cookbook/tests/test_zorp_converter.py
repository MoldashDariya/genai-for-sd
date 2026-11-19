import pytest

from zorp_converter import to_earth, zorp_number


@pytest.mark.parametrize(
    "measure, expected",
    [
        ("Zopity Zap globs", "2 cups"),
        ("Zam zapity globs", "3 cups"),
        ("Zoom zopity eggs", "8 eggs"),
        ("Zop zopity globs", "3 cups"),
        ("Zap zapity scoops", "3 scoops"),
        ("Zoom zapity bananas", "5 bananas"),
    ],
)
def test_recipe_measures(measure, expected):
    assert to_earth(measure) == expected


def test_numbers():
    assert [zorp_number([w]) for w in ["zip", "zap", "zop", "zoom", "zam"]] == [1, 2, 3, 4, 5]


def test_odd_globs_give_half_cups():
    assert to_earth("Zip globs") == "0.5 cups"


def test_unknown_word():
    with pytest.raises(ValueError):
        zorp_number(["zork"])
