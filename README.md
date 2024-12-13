# Dio

A rather tenuous name. Branding functions with a "created by AI" message and attributes to help identify them.

Brand -> Brando -> Dio Brando -> Dio -> [Za Warudo](https://jojo.fandom.com/wiki/The_World)

This is (currently: will be) a repository of useful functions and tools for working with code generated by AI tools. 


## Installation

Don't for now. I'll bundle up all the different languages into branches later.

## Installation

Each language's tools will live on their own branches. To install them use the instructions below.

### Python

I recommend managing `dio` as a dependency using [poetry](https://python-poetry.org/). You can add it to your project dependencies using

``` toml
[tool.poetry.dependencies]
dio = { git = "https://github.com/raisedbyfinches/dio.git", branch = "python" }
```

If this is not available, wheels and tar.gz archives will be distributed under releases.


## Usage

### AI generated code

When developing code with Copilot assistance we should mark all code written by it. To do so follow this example and apply it to your own codebase.

``` python
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

```

Import copilot from decorators.py and decorate your functions with `@copilot`. This is explicitly copilot as that's the tool available in my work setting. Other LLM origins are not supported *yet*.

This provides:

- A warning that a function call is using a function which was written with or by Microsoft Copilot, including the function call itself.
- Attributes to the function itself to better frame your questions when investigating the content.
  + Code complexity (via cyclomatic complexity computation)
  + Identification of long line and deeply nested (list + conditional) anti-patterns
  + System information for the system on which the function is called

