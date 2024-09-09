import itertools

def generate_unique_permutations(n, k):
    # Create the initial list with k ones and n-k zeros
    initial_list = [1] * k + [0] * (n - k)
    
    # Generate all unique permutations
    all_permutations = set(itertools.permutations(initial_list))
    
    # Function to generate cyclic permutations of a given permutation
    def generate_cyclic_permutations(perm):
        return {tuple(perm[i:] + perm[:i]) for i in range(len(perm))}
    
    unique_permutations = set()
    
    for perm in all_permutations:
        cyclic_perms = generate_cyclic_permutations(perm)
        smallest_perm = min(cyclic_perms)
        unique_permutations.add(smallest_perm)
    
    return unique_permutations

# Example usage
n = 9

total = 0
for k in range(n+1):
    unique_perms = generate_unique_permutations(n, k)
    total += len(unique_perms)
    print(f"Number of unique permutations for n={n}, k={k}: {len(unique_perms)}")

    # print("Unique permutations:")
    # for perm in unique_permutations:
    #     print(perm)

print(f"Total unique permutations for n={n}: {total}")
# 7 -> 20
# 9 -> 60
# 11 -> 188
