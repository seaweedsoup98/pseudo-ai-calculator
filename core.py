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
        "x": "X"
    }.get(str(value).lower())


def decide(a, b, label_a="A", label_b="B"):
    if abs(a - b) < EPSILON:
        return "UNDECIDED"
    return label_a if a > b else label_b


def mac_2d(pattern, filter_):
    return sum(
        sum(x * y for x, y in zip(r1, r2))
        for r1, r2 in zip(pattern, filter_)
    )


def flatten(matrix):
    return [v for r in matrix for v in r]


def mac_1d(pattern, filter_):
    return sum(x * y for x, y in zip(pattern, filter_))


def generate_pattern(n, label):
    label = normalize(label)
    if n < 1:
        raise ValueError("크기를 확인하세요")
    elif label is None:
        raise ValueError("라벨을 확인하세요")

    pattern = [[0.0] * n] * n
    middle = n // 2

    for i in range(n):
        if label == "Cross":
            pattern[middle][i] = pattern[i][middle] = 1.0
        else:
            pattern[i][i] = pattern[i][n - 1 - i] = 1.0

    return pattern

