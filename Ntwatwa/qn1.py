from itertools import combinations

maxno=20
def generate_combinations(n, k):
    if (n<1 or n>20 ) or (k<1 or k>n):
        print(f"{n} should be less than {maxno}" if n>20 else f"{k} should be less than {n}")
        print(f"--"*20)
        return []
    return list(combinations(range(1, n + 1), k))


n = int(input(f"Enter the value of n ({maxno}): "))
k = int(input(f"Enter the value of k (<{n}): "))
#Results
result = generate_combinations(n, k)
print(result    )