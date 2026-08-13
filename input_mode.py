from core import EPSILON, decide, generate_pattern, mac_2d, normalize
from performance import average_classification_time, print_performance


def input_matrix(name):
    print(f"{name} (3줄 입력, 공백 구분)")
    matrix = []

    while len(matrix) < 3:
        try:
            row = [float(value) for value in input().split()]

            if len(row) != 3:
                raise ValueError

            matrix.append(row)
        except ValueError:
            print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")

    return matrix


def input_pattern():
    while True:
        choice = input(
            "패턴 입력 방식 (1: 직접 입력, 2: 자동 생성): "
        ).strip()

        if choice == "1":
            return input_matrix("패턴")

        if choice == "2":
            label = normalize(input("패턴 종류 (Cross/X): ").strip())

            if label:
                pattern = generate_pattern(3, label)

                for row in pattern:
                    print(*row)

                return pattern

            print("Cross 또는 X를 입력하세요.")
            continue

        print("1 또는 2를 입력하세요.")


def run_input_mode():
    print("\n[1] 필터 입력")
    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")
    print("✓ 필터 A, B 저장 완료")

    print("\n[2] 패턴 입력")
    pattern = input_pattern()
    print("✓ 패턴 저장 완료")

    score_a = mac_2d(pattern, filter_a)
    score_b = mac_2d(pattern, filter_b)
    elapsed = average_classification_time(pattern, filter_a, filter_b)
    result = decide(score_a, score_b)

    print("\n[3] MAC 결과")
    print(f"A 점수: {score_a!r}")
    print(f"B 점수: {score_b!r}")
    print(f"연산 시간(평균/10회): {elapsed:.6f} ms")

    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"판정: {result}")

    print_performance((3,), 4)