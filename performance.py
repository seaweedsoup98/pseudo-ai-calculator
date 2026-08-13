import time
from core import flatten, generate_pattern, mac_1d, mac_2d

REPEAT = 10


def average_time(function, pattern, filter_):
    start = time.perf_counter()

    for _ in range(REPEAT):
        function(pattern, filter_)

    return (time.perf_counter() - start) * 1000 / REPEAT


def print_performance(sizes):
    print(f"\n[성능 분석] 평균/{REPEAT}회")
    print("크기\t2D 평균(ms)\t1D 평균(ms)\t연산 횟수")

    for n in sizes:
        pattern = generate_pattern(n, "Cross")
        filter_ = generate_pattern(n, "Cross")
        flat_pattern = flatten(pattern)
        flat_filter = flatten(filter_)

        # flatten 제외 MAC 함수 호출 구간만 측정
        before = average_time(mac_2d, pattern, filter_)
        after = average_time(mac_1d, flat_pattern, flat_filter)

        print(f"{n}x{n}\t{before:.6f}\t{after:.6f}\t{n * n}")