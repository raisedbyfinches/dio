"""
-*- Not to be run as a standalone program
-*- Minimum python version: 3.12

Decorators and functions to wrap code written by or with LLM support.
"""

# -- Libraries ------------------------------------------------------------------
# future
from __future__ import annotations

# base
import ast
import functools
import inspect
import itertools
import sys
import warnings

# named
from collections.abc import Callable
from typing import Any, TypeVar, ParamSpec, TypeAlias


# -- Types ----------------------------------------------------------------------


P = ParamSpec("P")
R = TypeVar("R")

# REVIEW: This was downgraded to be python 3.10 compliant, this requires
#         TypeAlias and Dict
# type Result = dict[str, Any]  # Analysis result for code complexity
Result: TypeAlias = dict[str, Any]


# -- Functions ------------------------------------------------------------------


def complexity(func: Callable[P, R]) -> float:
    """
    Calculate cyclomatic complexity using AST analysis

    :param func (Callable): Function to analyse
    :return float: Calculated complexity metric
    """
    source = inspect.getsource(func)
    tree = ast.parse(source)

    def analyse(node: ast.AST) -> int:
        """
        Recursively calculate complexity based on node types.
        """
        children = ast.iter_child_nodes(node)
        match node:
            case ast.If() | ast.While() | ast.For():
                return 1 + sum(analyse(child) for child in children)

            case ast.BoolOp(values=values):
                return len(values) - 1 + sum(analyse(child) for child in children)

            case ast.Try(handlers=handlers, finalbody=finalbody):
                return (
                    len(handlers)
                    + len(finalbody)
                    + sum(analyse(child) for child in children)
                )

            case _:
                return sum(analyse(child) for child in children)

    return 1 + analyse(tree)


def antipatterns(func: Callable[P, R]) -> Result:
    """
    Analyse functions for potential anti-patterns using pattern matching.

    :param func (Callable): Function to analyse
    :return Result: Dictionary of detected anti-patterns
    """
    tree = ast.parse(inspect.getsource(func))
    source = inspect.getsource(func).splitlines()

    def analyse(line: str) -> list[str]:
        """Match and identify patterns"""
        match line.strip():
            case line if "global " in line:
                return ["global_variable"]
            case line if "print(" in line and "debug" in line.lower():
                return ["debug_print"]
            case line if len(line) > 120:
                return ["long_line"]
            case _:
                return []

    anti_patterns = itertools.chain.from_iterable(analyse(line) for line in source)

    # cound complexity related anti-patterns
    def depth(node: ast.AST, acc: int = 0) -> tuple[int, int]:
        """Recursively analyse depth and nested conditionals"""
        nested = 0
        children = ast.iter_child_nodes(node)

        match node:
            case ast.If() | ast.While() | ast.For():
                nested += 1
                acc += 1

        # recursively process nodes
        for child in children:
            # acc will have had its +1 added above if it needs it
            child_depth, child_conditionals = depth(child, acc)
            acc = max(acc, child_depth)
            nested += child_conditionals

        return acc, nested

    # analyse the entire AST
    d, c = depth(tree)

    # combine antipatterns
    if d > 3:  # depth greater than 3
        anti_patterns = itertools.chain(anti_patterns, ["deep_nesting"])
    if c > 5:  # more than 5 chained conditionals
        anti_patterns = itertools.chain(anti_patterns, ["complex_conditionals"])

    return {
        "detected_patterns": set(anti_patterns),
        "max_nesting_depth": d,
        "conditional_depth": c,
    }


def compatibility() -> Result:
    """
    Analyse system and version compatibility.

    :return Result: System and version information
    """
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_implementation": sys.implementation.name,
        "platform": sys.platform,
        "max_int_bits": sys.maxsize.bit_length(),
        "default_encoding": sys.getdefaultencoding(),
    }


def copilot(
    verbose: bool = False, log_file: str | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A hof for analysing and marking AI-generated functions.

    :param verbose (bool, optional): Enable detailed output. Default = False.
    :param log_file (str, optional): Path to log file. Default = None.
    :returns Callable: Decorated function with additional attributes.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        @functools.lru_cache(maxsize=None)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # prepare analysis results
            cycles = complexity(func)
            anti_patterns = antipatterns(func)
            system = compatibility()

            # verbose output
            if verbose:
                print(f"Function: {func.__name__}")
                print(f"Complexity: {cycles}")
                print("Anti-pattern analysis: ")
                for k, v in anti_patterns.items():
                    print(f"  - {k}: {v}")
                print("System compatibility: ")
                for k, v in system.items():
                    print(f"  - {k}: {v}")

            # logging
            if log_file:
                with open(log_file, "a") as f:
                    f.write(f"\nFunction: {func.__name__} | ")
                    f.write(f"Complexity: {cycles} | ")
                    f.write(f"Anti-patterns: {anti_patterns}")

            # runtime warning
            warnings.warn(
                "\n\n⚠ NOTICE: This function was generated or assisted by an AI. Review your outputs thoroughly and do not use in production. ⚠",
                category=RuntimeWarning,
                stacklevel=2,
            )

            # execute the function
            result = func(*args, **kwargs)

            return result

        # Attach analysis as attributes to function
        wrapper.complexity = complexity(func)
        wrapper.anti_patterns = antipatterns(func)
        wrapper.system = compatibility()
        wrapper.is_ai_generated = True

        return wrapper

    return decorator


"""
Example usage


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
"""
