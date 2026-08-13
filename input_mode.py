from core import decide, generate_pattern, mac_2d, normalize
from performance import print_performance


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
    choice = input("패턴 입력 방식 (1: 직접 입력, 2: 자동 생성): ").strip()

    if choice != "2":
        return input_matrix("패턴")

    while True:
        label = normalize(input("패턴 종류 (Cross/X): ").strip())

        if label:
            pattern = generate_pattern(3, label)
            print("자동 생성된 3x3 패턴")
            for row in pattern:
                print(*row)
            return pattern

        print("Cross 또는 X를 입력하세요.")


def run_input_mode():
    print("\n[1] 필터 입력")
    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")
    print("필터 저장 완료")

    print("\n[2] 패턴 입력")
    pattern = input_pattern()
    print("패턴 저장 완료")

    score_a = mac_2d(pattern, filter_a)
    score_b = mac_2d(pattern, filter_b)
    result = decide(score_a, score_b)

    print("\n[3] MAC 결과")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print("판정:", "판정 불가" if result == "UNDECIDED" else result)

    print_performance((3,))