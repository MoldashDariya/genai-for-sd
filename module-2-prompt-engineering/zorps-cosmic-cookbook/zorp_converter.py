"""Translate Zorp's alien recipe measures into Earth measures.

Rules of Zorp's cookbook:
- numbers: Zip, Zap, Zop, Zoom, Zam = 1, 2, 3, 4, 5
- "zopity" doubles the number, "zapity" adds 1
- 1 glob = 0.5 cups
"""

NUMBERS = {"zip": 1, "zap": 2, "zop": 3, "zoom": 4, "zam": 5}
MODIFIERS = {"zopity": lambda n: n * 2, "zapity": lambda n: n + 1}
CUPS_PER_GLOB = 0.5

RECIPES = {
    "Cosmic Cookies": [
        ("Flour", "Zopity Zap globs"),
        ("Sugar", "Zam zapity globs"),
        ("Eggs", "Zoom zopity eggs"),
    ],
    "Martian Milkshake": [
        ("Milk", "Zop zopity globs"),
        ("Ice cream", "Zap zapity scoops"),
        ("Bananas", "Zoom zapity bananas"),
    ],
}


def zorp_number(words):
    """Return the value of a Zorp number phrase, e.g. ["zopity", "zap"] -> 4."""
    number = None
    modifiers = []
    for word in words:
        if word in NUMBERS:
            number = NUMBERS[word]
        elif word in MODIFIERS:
            modifiers.append(MODIFIERS[word])
        else:
            raise ValueError(f"Unknown Zorp word: {word}")
    if number is None:
        raise ValueError(f"No Zorp number in: {' '.join(words)}")
    for apply in modifiers:
        number = apply(number)
    return number


def to_earth(measure):
    """Convert a measure like "Zopity Zap globs" to an Earth measure like "2 cups"."""
    *number_words, unit = measure.lower().split()
    value = zorp_number(number_words)
    if unit == "globs":
        value, unit = value * CUPS_PER_GLOB, "cups"
    if value == int(value):
        value = int(value)
    return f"{value} {unit}"


def to_markdown(recipes=RECIPES):
    lines = []
    for name, ingredients in recipes.items():
        lines += [name, "", "| Ingredient | Zorp Measure | Earth Measure |", "|---|---|---|"]
        lines += [f"| {item} | {measure} | {to_earth(measure)} |" for item, measure in ingredients]
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(to_markdown())
