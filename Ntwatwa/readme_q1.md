# 🔢 Combination Generator

This Python script generates all possible combinations of `k` elements from a set of integers ranging from `1` to `n`, using the built-in `itertools.combinations` function.

## 📋 Features

- Validates input to ensure `n` and `k` are within acceptable bounds.
- Uses Python's `itertools` to efficiently compute combinations.
- Provides user-friendly prompts and error messages.

## 🧠 How It Works

1. Prompts the user to enter values for `n` and `k`.
2. Validates that:
   - `1 ≤ n ≤ 20`
   - `1 ≤ k ≤ n`
3. If valid, prints all combinations of `k` elements from the set `{1, 2, ..., n}`.

## 🖥️ Usage

Run the script in a Python environment:

```bash
python combination_generator.py

