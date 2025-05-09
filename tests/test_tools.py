# ruff: noqa: PLW2901
from typing import Never

import pytest

from monads.exceptions import UnwrapError
from monads.option import Null, Option, Some
from monads.result import Err, Ok, Result
from monads.tools import (
    CatchResult,
    collect_options,
    collect_results,
    from_none,
    try_option,
    try_result,
)


def _throw(exc: type[BaseException], /) -> Never:
    raise exc


def test_catch_ok() -> None:
    value = "123"

    with CatchResult(ValueError) as catch:
        catch @= int(value)

    assert catch.result == Ok(123)


def test_catch_err() -> None:
    value = "abc"

    with CatchResult(ValueError) as catch:
        catch @= int(value)

    result = catch.result
    assert type(result) is Err
    assert type(result.err_value) is ValueError


def test_catch_matmul_not_called() -> None:
    with CatchResult(ValueError) as catch:
        pass

    with pytest.raises(UnwrapError):
        _ = catch.result


def test_catch_does_not_swallow() -> None:
    with pytest.raises(TypeError), CatchResult(ValueError):
        raise TypeError


def test_try_result_ok() -> None:
    result = try_result(int, ValueError, "123")
    assert result == Ok(123)


def test_try_result_err() -> None:
    result = try_result(int, ValueError, "abc")
    assert type(result) is Err
    assert type(result.err_value) is ValueError


def test_try_result_does_not_swallow() -> None:
    with pytest.raises(RuntimeError):
        _ = try_result(_throw, TypeError, RuntimeError)


def test_try_option_some() -> None:
    option = try_option(int, ValueError, "123")
    assert option == Some(123)


def test_try_option_null() -> None:
    option = try_option(int, ValueError, "abc")
    assert option == Null.null


def test_try_option_does_not_swallow() -> None:
    with pytest.raises(RuntimeError):
        _ = try_option(_throw, ValueError, RuntimeError)


def test_from_none() -> None:
    assert from_none(None) == Null.null
    assert from_none(123) == Some(123)


@pytest.mark.parametrize(
    ("options", "result"),
    [
        ([Some(1), Some(2), Some(3)], Some([1, 2, 3])),
        ([Some(1), Null.null, Some(3)], Null.null),
    ],
)
def test_collect_options[T](options: list[Option[T]], result: Option[list[T]]) -> None:
    assert collect_options(options) == result


@pytest.mark.parametrize(
    ("results", "result"),
    [
        ([Ok(1), Ok(2), Ok(3)], Ok([1, 2, 3])),
        ([Ok(1), Err("foo"), Ok(3)], Err("foo")),
    ],
)
def test_collect_results[T, E](results: list[Result[T, E]], result: Result[list[T], E]) -> None:
    assert collect_results(results) == result
