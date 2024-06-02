def hanoi_4_rods(n):
    T = [float('inf')] * (n + 1)
    T[0] = 0
    T[1] = 1
    
    for i in range(2, n + 1):
        for k in range(1, i):
            T[i] = min(T[i], 2 * T[k] + T[i - k])
    
    return T

import sys

def main():
    input = sys.stdin.read().strip()
    test_cases = list(map(int, input.split()))
    max_n = max(test_cases)
    T = hanoi_4_rods(max_n)
    
    for i, n in enumerate(test_cases):
        print(f"Case {i + 1}: {T[n]}")

if __name__ == "__main__":
    main()
