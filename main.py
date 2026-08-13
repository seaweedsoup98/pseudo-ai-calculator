from input_mode import run_input_mode
from json_mode import run_json_mode


def main():
    print("=== Mini NPU Simulator ===")

    while True:
        choice = input(
            "\n1. 사용자 입력 (3x3)\n"
            "2. data.json 분석\n"
            "선택: "
        ).strip()

        if choice == "1":
            run_input_mode()
            break

        if choice == "2":
            run_json_mode()
            break

        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()