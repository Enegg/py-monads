"""Tools for converting into `Option` & `Result`.

Copyright (c) 2024-present Eneg
"""

from collections import abc
from typing import Never, Protocol, Self, overload

import attrs

from monads.option import Null, Option, Some
from monads.result import Err, Ok, Result

__all__ = (
    "CatchResult",
    "collect_options",
    "collect_results",
    "from_none",
    "try_option",
    "try_result",
)


class HasResult[T, E](Protocol):
    @property
    def result(self) -> Ok[T, E]: ...


@attrs.frozen
class _Success[T]:
    result: Ok[T]


@attrs.define
class CatchResult[ExcT: BaseException]:
    """Context manager catching exceptions into `Result` type.

    ```
    with CatchResult(ValueError) as catch:
        catch @= int("123")

    print(catch.result)  # Ok(123) | Err(ValueError(...))
    ```
    """

    excs: tuple[type[ExcT], ...]
    _result: Option[ExcT]

    def __init__(self, *excs: type[ExcT]) -> None:
        self.excs = excs
        self._result = Null.null

    def __enter__(self) -> Self:
        return self

    def __exit__(self, _: object, exc: BaseException | None, __: object) -> bool:
        if exc is not None and isinstance(exc, self.excs):
            self._result = Some(exc)
            return True

        return False

    def __imatmul__[U](self, value: U, /) -> HasResult[U, ExcT]:  # noqa: PYI034
        return _Success(Ok(value))

    @property
    def result(self) -> Err[ExcT, Never]:
        return self._result.map(Err).unwrap("No exception caught and @= not called")


def try_result[ExcT: BaseException, **P, T](
    f: abc.Callable[P, T],
    exc: type[ExcT] | tuple[type[ExcT], ...],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, ExcT]:
    """Run callable `(...) -> T`, return `Ok[T]` on success, or `Err[Exception]` on exception."""
    try:
        return Ok(f(*args, **kwargs))

    except exc as err:
        return Err(err)


def try_option[**P, T](
    f: abc.Callable[P, T],
    exc: type[BaseException] | tuple[type[BaseException], ...],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Option[T]:
    """Run callable `(...) -> T`, return `Some[T]` on success, or `Null` on exception."""
    try:
        return Some(f(*args, **kwargs))

    except exc:
        return Null.null


@overload
def from_none(obj: None, /) -> Null: ...
@overload
# ideally this'd be [T: object & ~None] -> Some[T]
def from_none[T](obj: T | None, /) -> Option[T]: ...
def from_none[T](obj: T | None, /) -> Option[T]:
    """Turn `T | None` into `Option[T]`."""
    return Null.null if obj is None else Some(obj)


def collect_options[T](it: abc.Iterable[Option[T]], /) -> Option[list[T]]:
    """Collect an iterable of `Option`s into a `list` of contained values.

    ```
    options = [Some(2), Some(4), Null.null, Some(8)]
    values = collect_options(options)
    assert values is Null.null

    options = [Some(2), Some(4), Some(8)]
    values = collect_options(options)
    assert values == Some([1, 2, 3])
    ```

    Returns
    -------
        `Some[list[T]]` if none of the elements is `Null`, else `Null`.
    """
    values: list[T] = []

    for o in it:
        if not o:
            return Null.null

        values.append(o.value)

    return Some(values)


def collect_results[T, E](it: abc.Iterable[Result[T, E]], /) -> Result[list[T], E]:
    """Collect an iterable of `Result`s into a `list` of contained values.

    ```
    results = [Ok(2), Ok(4), Err("no"), Ok(8), Err("yes")]
    values = collect_results(results)
    assert values == Err("no")

    results = [Ok(2), Ok(4), Ok(8)]
    values = collect_results(results)
    assert values == Ok([1, 2, 3])
    ```

    Returns
    -------
        `Ok[list[T]]` if none of the elements is `Err`, else the first `Err[E]`.
    """
    values: list[T] = []

    for r in it:
        if not r:
            return Err(r.err_value)

        values.append(r.ok_value)

    return Ok(values)
