from collections import abc
from typing import Generic, Protocol, overload
from typing_extensions import Self

import attrs

from monads.option import Null, Option, Some
from monads.result import Err, Ok, Result
from monads.types import ExcT, P, T, U

__all__ = ("CatchResult", "from_none", "try_option", "try_result")


class HasResult(Protocol[U]):
    @property
    def result(self) -> Ok[U]: ...


@attrs.frozen
class _Success(Generic[U]):
    result: Ok[U]


@attrs.define
class CatchResult(Generic[ExcT]):
    """Context manager catching exceptions into Result type.

    ### Usage:

    ```
    with CatchResult(ValueError) as catch:
        catch @= int("12345")

    reveal_type(catch.result)  # Result[int, ValueError]
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

    def __imatmul__(self, value: U, /) -> HasResult[U]:  # noqa: PYI034
        return _Success(Ok(value))

    @property
    def result(self) -> Err[ExcT]:
        return self._result.map(Err).unwrap("No exception caught and @= not called")


def try_result(
    f: abc.Callable[P, T],
    exc: type[ExcT] | tuple[type[ExcT], ...],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Result[T, ExcT]:
    try:
        return Ok(f(*args, **kwargs))

    except exc as err:
        return Err(err)


def try_option(
    f: abc.Callable[P, T],
    exc: type[BaseException] | tuple[type[BaseException], ...],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Option[T]:
    """Run callable `(...) -> T`, return `Some(T)` on success, or `Null` on exception."""
    try:
        return Some(f(*args, **kwargs))

    except exc:
        return Null.null


@overload
def from_none(obj: None, /) -> Null: ...
@overload
def from_none(obj: T | None, /) -> Option[T]: ...
def from_none(obj: T | None, /) -> Option[T]:
    """Turn `T | None` into `Option[T]`."""
    return Null.null if obj is None else Some(obj)
