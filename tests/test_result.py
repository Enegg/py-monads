import pytest

from monads.result import Err, Ok, Result


def test_eq() -> None:
    assert Ok(1) == Ok(1)
    assert Ok(1) != Ok(2)
    assert Err("1") == Err("1")
    assert Err("1") != Err("2")
    assert Ok(1) != Err(1)
    assert Ok(1) != 1


def test_match_ok() -> None:
    match Ok(1):
        case Err(1):  # pyright: ignore[reportUnnecessaryComparison]
            pytest.fail("Ok should not match Err")

        case Ok(1):
            pass

        case _:
            pytest.fail("Ok(1) should not fall through case Ok(1)")


def test_match_err() -> None:
    match Err("1"):
        case Ok("1"):  # pyright: ignore[reportUnnecessaryComparison]
            pytest.fail("Err should not match Ok")

        case Err("1"):
            pass

        case _:
            pytest.fail("Err('1') should not fall through case Err('1')")


@pytest.mark.parametrize(
    ("lhs", "rhs", "lhs_t", "rhs_t"),
    [
        (Ok(1), Ok(1), (0, 1), (0, 1)),
        (Ok(1), Ok(2), (0, 1), (0, 2)),
        (Ok(2), Ok(1), (0, 2), (0, 1)),
        (Err("1"), Err("1"), (1, 1), (1, 1)),
        (Err("1"), Err("2"), (1, 1), (1, 2)),
        (Err("2"), Err("1"), (1, 2), (1, 1)),
        (Ok(1), Err("1"), (0, 1), (1, 1)),
        (Err("1"), Ok(1), (1, 1), (0, 1)),
    ],
)
def test_rich_comparison(
    lhs: Result[int, str], rhs: Result[int, str], lhs_t: tuple[int, int], rhs_t: tuple[int, int]
) -> None:
    assert (lhs > rhs) == (lhs_t > rhs_t)
    assert (lhs >= rhs) == (lhs_t >= rhs_t)
    assert (lhs < rhs) == (lhs_t < rhs_t)
    assert (lhs <= rhs) == (lhs_t <= rhs_t)
