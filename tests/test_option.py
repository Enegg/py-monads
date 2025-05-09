import pytest

from monads.option import Null, Option, Some


def test_eq() -> None:
    assert Some(1) == Some(1)
    assert Some(1) != Some(2)
    assert Some(1) != Null.null
    assert Null.null == Null.null
    assert Null.null is Null[int]()
    assert Some(1) != 1


def test_match_null() -> None:
    match Null.null:
        case Some():  # pyright: ignore[reportUnnecessaryComparison]
            pytest.fail("Null should not match to Some")

        case Null.null:
            pass

        case _:
            pytest.fail("Null should not fall through case Null.null")


@pytest.mark.parametrize(("some", "expected"), [(Some(1), 1), (Some("123"), "123")])
def test_match_some[T](some: Some[T], expected: T) -> None:
    match some:
        case Null.null:
            pytest.fail("Some should not match to Null")

        case Some(value):
            assert expected == value

        case _:
            pytest.fail("Some should not fall through case Some(value)")


@pytest.mark.parametrize(
    ("lhs", "rhs", "expected"),
    [
        (Some(1), Some(2), Null.null),
        (Some(1), Null.null, Some(1)),
        (Null.null, Some(1), Some(1)),
        (Null.null, Null.null, Null.null),
    ],
)
def test_xor(lhs: Option[int], rhs: Option[int], expected: Option[int]) -> None:
    assert lhs.xor(rhs) == expected


@pytest.mark.parametrize(
    ("lhs", "rhs", "lhs_t", "rhs_t"),
    [
        (Some(1), Some(1), (1, 1), (1, 1)),
        (Some(1), Some(2), (1, 1), (1, 2)),
        (Some(2), Some(1), (1, 2), (1, 1)),
        (Null.null, Null.null, (0,), (0,)),
        (Some(1), Null.null, (1, 1), (0,)),
        (Null.null, Some(0), (0,), (1, 0)),
    ],
)
def test_rich_comparison(
    lhs: Option[int], rhs: Option[int], lhs_t: tuple[int, ...], rhs_t: tuple[int, ...]
) -> None:
    assert (lhs > rhs) == (lhs_t > rhs_t)
    assert (lhs >= rhs) == (lhs_t >= rhs_t)
    assert (lhs < rhs) == (lhs_t < rhs_t)
    assert (lhs <= rhs) == (lhs_t <= rhs_t)
