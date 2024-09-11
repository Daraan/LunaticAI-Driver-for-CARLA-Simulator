from __future__ import annotations

__all__ = [
    'get_car_coords',
]


def get_car_coords(matrix) -> tuple[int, int]:
    """
    Position of the ego vehicle in the matrix.
    Should be a constant value for non-junctions.
    """
    (i_car, j_car) = (0, 0)
    for lane, occupations in matrix.items():
        try:
            return (lane, occupations.index(1))  # find the 1 entry in a efficient way
        except ValueError:  # noqa: PERF203
            continue

    return i_car, j_car
