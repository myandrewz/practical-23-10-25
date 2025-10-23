# Combinations Problem Solution

A Python implementation that generates all possible combinations of k numbers chosen from the range [1, n].

## 🎯 Problem Statement

Given two integers `n` and `k`, return all possible combinations of `k` numbers chosen from the range `[1, n]`. The order of combinations doesn't matter.

### Example:
- **Input**: `n = 4, k = 2`
- **Output**: `[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]`

## 🚀 Features

- **Backtracking Algorithm**: Efficient recursive solution using backtracking
- **Alternative Iterative Solution**: Using Python's `itertools.combinations`
- **Comprehensive Testing**: Multiple test cases including edge cases
- **Formatted Output**: Clean display of results with total count
- **Input Validation**: Handles edge cases like `k=0`, `k>n`

## 📋 Requirements

- Python 3.6+
- No external dependencies (uses only built-in libraries)

## 🛠️ Installation & Usage

### 1. Navigate to the Directory

```bash
cd qn1
```

### 2. Run the Solution

```bash
python combinations.py
```

### 3. Using as a Module

```python
from combinations import combine, combine_iterative, print_combinations

# Generate combinations
result = combine(4, 2)
print(result)  # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

# Print formatted output
print_combinations(4, 2)

# Alternative iterative approach
result_iter = combine_iterative(4, 2)
```

## 🔧 Functions

### `combine(n, k)`
**Main backtracking solution**
- **Parameters**: 
  - `n` (int): Upper bound of the range [1, n]
  - `k` (int): Number of elements in each combination
- **Returns**: `List[List[int]]` - List of all possible combinations
- **Time Complexity**: O(C(n,k) * k) where C(n,k) is the binomial coefficient
- **Space Complexity**: O(C(n,k) * k) for storing all combinations

### `combine_iterative(n, k)`
**Alternative solution using itertools**
- **Parameters**: Same as `combine()`
- **Returns**: Same as `combine()`
- **Advantage**: More concise, leverages built-in optimized library

### `print_combinations(n, k)`
**Formatted output function**
- **Parameters**: Same as `combine()`
- **Returns**: `List[List[int]]` and prints formatted results
- **Features**: Shows total count and formatted display
