from typing import List

def matrix_multiplication(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    result = []

    # Populate the result matrix with zeros
    for i in range(0, len(a)):
        result.append([])
        for j in range(0, len(b[0])):
            result[i].append(0)

    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]

    return result