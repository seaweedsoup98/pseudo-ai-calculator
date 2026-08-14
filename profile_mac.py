import cProfile
import dis
import pstats
import sys
import timeit
import tracemalloc
from collections import Counter

from core import flatten, generate_pattern, mac_1d, mac_2d

SIZES = (25, 100, 250)
REPEAT = 5
TARGET_CELLS = 1_000_000


def mac_2d_cached(pattern, filter_):
    score = 0.0

    for i in range(len(pattern)):
        p_row = pattern[i]
        f_row = filter_[i]

        for j in range(len(p_row)):
            score += p_row[j] * f_row[j]

    return score


def measure(function, pattern, filter_, n):
    number = max(1, TARGET_CELLS // (n * n))

    for _ in range(20):
        function(pattern, filter_)

    times = timeit.repeat(
        lambda: function(pattern, filter_),
        number=number,
        repeat=REPEAT,
    )

    return number, [time * 1000 / number for time in times]


def benchmark():
    print("\n[1] timeit benchmark")
    print("size\tmethod\t\tbest(ms)\tcalls")

    for n in SIZES:
        matrix = generate_pattern(n, "Cross")
        flat = flatten(matrix)

        methods = (
            ("2D", mac_2d, matrix),
            ("2D cached", mac_2d_cached, matrix),
            ("1D", mac_1d, flat),
        )

        for name, function, data in methods:
            number, times = measure(function, data, data, n)
            print(f"{n}\t{name:<10}\t{min(times):.6f}\t{number}")


def bytecode():
    print("\n[2] bytecode structure")

    for function in (mac_2d, mac_2d_cached, mac_1d):
        counts = Counter(
            instruction.opname
            for instruction in dis.get_instructions(function)
        )

        print(
            f"{function.__name__}: "
            f"FOR_ITER={counts['FOR_ITER']}, "
            f"BINARY_SUBSCR={counts['BINARY_SUBSCR']}, "
            f"BINARY_OP={counts['BINARY_OP']}"
        )


def profile():
    print("\n[3] cProfile")

    n = 250
    matrix = generate_pattern(n, "Cross")
    flat = flatten(matrix)

    for name, function, data in (
        ("2D", mac_2d, matrix),
        ("1D", mac_1d, flat),
    ):
        profiler = cProfile.Profile()
        profiler.enable()

        for _ in range(20):
            function(data, data)

        profiler.disable()

        print(f"\n{name}")
        pstats.Stats(profiler).sort_stats("tottime").print_stats(5)


def memory():
    print("\n[4] memory")

    matrix = generate_pattern(500, "Cross")
    matrix_bytes = (
        sys.getsizeof(matrix)
        + sum(sys.getsizeof(row) for row in matrix)
    )

    tracemalloc.start()
    flat = flatten(matrix)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"2D list containers: {matrix_bytes / 1024:.1f} KiB")
    print(f"flat list container: {sys.getsizeof(flat) / 1024:.1f} KiB")
    print(f"flatten additional peak: {peak / 1024:.1f} KiB")


if __name__ == "__main__":
    print(sys.version)
    benchmark()
    bytecode()
    profile()
    memory()