from itertools import combinations

def generate_combinations(n, k):
    
    result = list(combinations(range(1, n + 1), k))
    
    result = [list(combo) for combo in result]
    
    return result


if __name__ == "__main__":
    print("=== combinationn generetor program ===")
    print("Constraints: 1 <= n <= 20, 1 <= k <= n\n")
    
    while True:
        try:
            n = int(input("Enter n: "))
            
            
            if not (1 <= n <= 20):
                print("error: n must be between 1 and 20.\n")
                continue
            
            
            k = int(input("enter k (number of elements in combination): "))
            
            
            if not (1 <= k <= n):
                print(f"Error: k must be between 1 and {n}..\n")
                continue
            
            
            result = generate_combinations(n, k)
            print(f"\nCombinations for n={n}, k={k}:")
            print(result)
            print(f"\nTotal number of combinattions: {len(result)}")
            break
            
        except ValueError:
            print("esrror: please enter valid integers\n")
        except KeyboardInterrupt:
            print("\n\nProgram has closed by user.")
            break