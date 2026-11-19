# Zorp's Cosmic Cookbook Challenge

**Task:** Zorp, an alien chef, writes recipes with alien numbers and measures. Translate two recipes
(Cosmic Cookies, Martian Milkshake) into Earth measures. The answer must contain only tables with the columns
`Ingredient`, `Zorp Measure`, `Earth Measure`, without a prompt.

Rules: Zip, Zap, Zop, Zoom, Zam = 1…5; *zopity* doubles the number; *zapity* adds 1; 1 glob = 0.5 cups.

**Score:** 100 / 100 (1st attempt)

## Submitted solution

Recipe 1: Cosmic Cookies

| Ingredient | Zorp Measure | Earth Measure |
|---|---|---|
| Flour | Zopity Zap globs | 2 cups |
| Sugar | Zam zapity globs | 3 cups |
| Eggs | Zoom zopity eggs | 8 eggs |

Recipe 2: Martian Milkshake

| Ingredient | Zorp Measure | Earth Measure |
|---|---|---|
| Milk | Zop zopity globs | 3 cups |
| Ice cream | Zap zapity scoops | 3 scoops |
| Bananas | Zoom zapity bananas | 5 bananas |

## How the numbers were checked

| Zorp Measure | Calculation | Earth Measure |
|---|---|---|
| Zopity Zap globs | 2 × 2 = 4 globs × 0.5 | 2 cups |
| Zam zapity globs | 5 + 1 = 6 globs × 0.5 | 3 cups |
| Zoom zopity eggs | 4 × 2 | 8 eggs |
| Zop zopity globs | 3 × 2 = 6 globs × 0.5 | 3 cups |
| Zap zapity scoops | 2 + 1 | 3 scoops |
| Zoom zapity bananas | 4 + 1 | 5 bananas |

[`zorp_converter.py`](zorp_converter.py) applies the rules and prints the tables above;
[`tests/test_zorp_converter.py`](tests/test_zorp_converter.py) checks every conversion.

```bash
python zorp_converter.py
python -m pytest
```
