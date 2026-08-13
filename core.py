EPSILON = 1e-9


def valid_matrix(matrix, n):
    return (
        isinstance(matrix, list)
        and len(matrix) == n
        and all(
            isinstance(row, list)
            and len(row) == n
            and all(isinstance(value, (int, float)) for value in row)
            for row in matrix
        )
    )


def normalize(value):
    return {
        "+": "Cross",
        "cross": "Cross",
        "x": "X",
    }.get(str(value).lower())


def decide(a, b, label_a="A", label_b="B"):
    if abs(a - b) < EPSILON:
        return "UNDECIDED"
    return label_a if a > b else label_b


def mac_2d(pattern, filter_):
    score = 0.0
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_[i][j]
    return score


def flatten(matrix):
    return [value for row in matrix for value in row]


def mac_1d(pattern, filter_):
    score = 0.0
    for i in range(len(pattern)):
        score += pattern[i] * filter_[i]
    return score


def generate_pattern(n, label):
    label = normalize(label)

    if n < 1:
        raise ValueError("크기를 확인하세요.")
    if label is None:
        raise ValueError("라벨을 확인하세요.")

    pattern = [[0.0] * n for _ in range(n)]
    middle = n // 2

    for i in range(n):
        if label == "Cross":
            pattern[middle][i] = pattern[i][middle] = 1.0
        else:
            pattern[i][i] = pattern[i][n - 1 - i] = 1.0

    return pattern