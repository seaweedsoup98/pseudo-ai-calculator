import json
import re

from core import decide, mac_2d, normalize, valid_matrix
from performance import print_performance

SIZES = (5, 13, 25)


def load_data():
    try:
        with open("data/data.json", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("최상위 데이터가 객체가 아닙니다.")

        return data
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"data.json 로드 실패: {error}")
        return None


def load_filters(data):
    source = data.get("filters", {})
    filters = {}

    print("\n[1] 필터 로드")

    for n in SIZES:
        raw = source.get(f"size_{n}", {}) if isinstance(source, dict) else {}
        normalized = {
            normalize(key): value
            for key, value in raw.items()
            if normalize(key)
        } if isinstance(raw, dict) else {}

        if all(valid_matrix(normalized.get(label), n) for label in ("Cross", "X")):
            filters[n] = normalized
            print(f"size_{n}: Cross, X 로드 완료")
        else:
            print(f"size_{n}: 로드 실패 (필터 누락 또는 크기/형식 오류)")

    return filters


def validate_case(case_id, case, filters):
    match = re.fullmatch(r"size_(\d+)_\d+", case_id)

    if not match:
        return None, None, None, "패턴 키 형식 오류"

    if not isinstance(case, dict):
        return None, None, None, "패턴 항목 형식 오류"

    n = int(match.group(1))
    pattern = case.get("input")
    expected = normalize(case.get("expected"))

    if n not in filters:
        return None, None, None, "해당 크기 필터 누락 또는 오류"

    if not valid_matrix(pattern, n):
        return None, None, None, f"패턴 크기/형식 오류: {n}x{n} 필요"

    if expected is None:
        return None, None, None, "expected 라벨 오류"

    return pattern, expected, filters[n], None


def analyze_case(case_id, case, filters):
    pattern, expected, filter_, reason = validate_case(case_id, case, filters)

    print(f"\n--- {case_id} ---")

    if reason:
        print(f"FAIL ({reason})")
        return False, reason

    cross_score = mac_2d(pattern, filter_["Cross"])
    x_score = mac_2d(pattern, filter_["X"])
    result = decide(cross_score, x_score, "Cross", "X")
    passed = result == expected

    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")
    print(f"판정: {result} | expected: {expected} | {'PASS' if passed else 'FAIL'}")

    return passed, None if passed else f"판정 {result}, expected {expected}"


def run_json_mode():
    data = load_data()

    if data is None:
        return

    filters = load_filters(data)
    patterns = data.get("patterns", {})

    if not isinstance(patterns, dict):
        print("patterns 스키마 오류")
        return

    print("\n[2] 패턴 분석")
    failures = []

    for case_id, case in patterns.items():
        passed, reason = analyze_case(case_id, case, filters)

        if not passed:
            failures.append((case_id, reason))

    print_performance((3, 5, 13, 25))

    print("\n[4] 결과 요약")
    print(f"총 테스트: {len(patterns)}개")
    print(f"통과: {len(patterns) - len(failures)}개")
    print(f"실패: {len(failures)}개")

    if failures:
        print("실패 케이스:")
        for case_id, reason in failures:
            print(f"- {case_id}: {reason}")