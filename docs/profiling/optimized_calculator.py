import numpy as np
from signal_processing_algorithms.e_divisive.base import EDivisiveCalculator
from signal_processing_algorithms.e_divisive.calculators import numpy_calculator as EDivisive


class OptimizedCalculator(EDivisiveCalculator):
    @staticmethod
    def calculate_diffs(series: np.ndarray) -> np.ndarray:
        return EDivisive.calculate_diffs(series)

    @staticmethod
    def calculate_qhat_values(diffs: np.ndarray) -> np.ndarray:
        length = len(diffs)
        qhat_values = np.zeros(length, dtype=np.float)
        if length < 5:
            return qhat_values
        n = 2
        m = length - n

        term1 = sum(diffs[i][j] for i in range(n) for j in range(n, length))
        term2 = sum(diffs[i][k] for i in range(n) for k in range(i + 1, n))
        term3 = sum(diffs[j][k] for j in range(n, length) for k in range(j + 1, length))

        qhat_values[n] = EDivisive._calculate_q(term1, term2, term3, m, n)

        for n in range(3, (length - 2)):
            m = length - n
            # update term 1
            row_delta = sum(diffs[n - 1][y] for y in range(n - 1))
            column_delta = sum(diffs[y][n - 1] for y in range(n, length))

            term1 = term1 - row_delta + column_delta
            term2 = term2 + row_delta
            term3 = term3 - column_delta

            qhat_values[n] = EDivisive._calculate_q(term1, term2, term3, m, n)
        return qhat_values