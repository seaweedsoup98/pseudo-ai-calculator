import time

from core import flatten, generate_pattern, mac_1d, mac_2d

REPEAT = 10


def average_time(function, pattern, filter_):
    total = 0.0

    for _ in range(REPEAT):
        start = time.perf_counter()
        function(pattern, filter_)
        total += time.perf_counter() - start

    return total * 1000 / REPEAT


def average_classification_time(pattern, filter_a, filter_b):
    total = 0.0

    for _ in range(REPEAT):
        start = time.perf_counter()
        mac_2d(pattern, filter_a)
        mac_2d(pattern, filter_b)
        total += time.perf_counter() - start

    return total * 1000 / REPEAT


def print_performance(sizes, section):
    results = []

    for n in sizes:
        pattern = generate_pattern(n, "Cross")
        filter_ = generate_pattern(n, "Cross")
        flat_pattern = flatten(pattern)
        flat_filter = flatten(filter_)

        before = average_time(mac_2d, pattern, filter_)
        after = average_time(mac_1d, flat_pattern, flat_filter)

        results.append((n, before, after))

    print(f"\n[{section}] 성능 분석 (평균/{REPEAT}회)")
    print(f"{'크기(N×N)':<12}{'평균 시간(ms)':>16}{'연산 횟수(N²)':>16}")

    for n, before, _ in results:
        print(f"{n}×{n:<9}{before:>16.6f}{n * n:>16}")

    print(f"\n[보너스] 1차원 최적화 비교 (평균/{REPEAT}회)")
    print(f"{'크기(N×N)':<12}{'최적화 전(ms)':>16}{'최적화 후(ms)':>16}")

    for n, before, after in results:
        print(f"{n}×{n:<9}{before:>16.6f}{after:>16.6f}")