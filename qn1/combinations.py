"""
Combinations Problem Solution

Given two integers n and k, return all possible combinations of k numbers 
chosen from the range [1, n]. The order of combinations doesn't matter.
"""

def combine(n, k):
    """
    Generate all possible combinations of k numbers from range [1, n].
    
    Args:
        n (int): Upper bound of the range [1, n]
        k (int): Number of elements in each combination
    
    Returns:
        List[List[int]]: List of all possible combinations
    """
    result = []
    
    def backtrack(start, current_combination):
        """
        Backtracking helper function to generate combinations.
        
        Args:
            start (int): Starting number for current iteration
            current_combination (List[int]): Current combination being built
        """
        # Base case: if we have k numbers, add to result
        if len(current_combination) == k:
            result.append(current_combination[:])  
            return
        
        # Try all numbers from start to n
        for i in range(start, n + 1):
            # Add current number to combination
            current_combination.append(i)
            
            # Recursively build rest of combination
            # Use i+1 as start to avoid duplicates and maintain order
            backtrack(i + 1, current_combination)
            
            # Backtrack: remove current number
            current_combination.pop()
    
    backtrack(1, [])
    return result


def combine_iterative(n, k):
    """
    Alternative iterative solution using the itertools library.
    
    Args:
        n (int): Upper bound of the range [1, n]
        k (int): Number of elements in each combination
    
    Returns:
        List[List[int]]: List of all possible combinations
    """
    from itertools import combinations
    return [list(combo) for combo in combinations(range(1, n + 1), k)]


def print_combinations(n, k):
    """
    Print combinations in a formatted way for easy reading.
    
    Args:
        n (int): Upper bound of the range [1, n]
        k (int): Number of elements in each combination
    """
    result = combine(n, k)
    print(f"Combinations of {k} numbers from range [1, {n}]:")
    print(f"Total combinations: {len(result)}")
    print("Combinations:", result)
    return result


if __name__ == "__main__":
    # Test the example case
    print("=" * 50)
    print("COMBINATIONS PROBLEM SOLUTION")
    print("=" * 50)
    
    # Use the example to ensure it works correctly
    n, k = 4, 2
    print(f"\nExample: n = {n}, k = {k}")
    result = print_combinations(n, k)
    
    # Verify expected output
    expected = [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
    print(f"\nExpected: {expected}")
    print(f"Got:      {result}")
    print(f"Match: {result == expected}")
    
    print("\n" + "=" * 50)
    print("ADDITIONAL TEST CASES")
    print("=" * 50)
    
    # Additional test cases
    test_cases = [
        (5, 3),  # More complex case
        (3, 1),  # Simple case with k=1
        (4, 4),  # Edge case where k=n
        (5, 0),  # Edge case with k=0
    ]
    
    for n, k in test_cases:
        print(f"\nTest case: n = {n}, k = {k}")
        if k == 0:
            print("Combinations of 0 numbers: [[]]")
        elif k > n:
            print("Invalid: k > n, no combinations possible")
        else:
            print_combinations(n, k)