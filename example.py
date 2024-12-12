#!/usr/bin/env python3

from dio import copilot


@copilot(verbose=True)
def add(x, y):
    return x + y


@copilot()
def example(x: int, y: int) -> int:
    "Demo."
    result = 0
    for _ in range(x):
        if y > 0:
            if y < 10:
                result += y
            else:
                result *= y
        else:
            result -= y

    return result


@copilot(verbose=True, log_file="./log.txt")
def example_(x: int, y: int) -> int:
    "Demo."
    result = 0
    for _ in range(x):
        if y:
            result += y

    return result


if __name__ == "__main__":
    simple = add(3, 5)
    result = example(3, 5)
    result_ = example_(3, 5)

    print(f"\nResult: {result}")
    print("\nFunction metadata:")
    print(f"    - Complexity: {example.complexity}")
    print(f"    - Anti-patterns: {example.anti_patterns}")
    print(f"    - System info: {example.system}")

    print(f"\nResult: {result_}")
    print("\nFunction metadata:")
    print(f"    - Complexity: {example_.complexity}")
    print(f"    - Anti-patterns: {example_.anti_patterns}")
    print(f"    - System info: {example_.system}")
