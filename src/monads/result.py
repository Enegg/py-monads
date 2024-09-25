# pyright: reportImportCycles=false

from collections import abc
from typing import TYPE_CHECKING, Final, Literal, Protocol, TypeAlias, final
from typing_extensions import Never, Self, override

import attrs

from monads.exceptions import UnwrapError
from monads.types import D, E, ExcT, F, Factory, P, Predicate, T, U

if TYPE_CHECKING:
    from monads.option import Null, Option, Some

__all__ = ("Err", "Ok", "Result", "try_result")


class _Result(Protocol[T, E]):
    __slots__ = ()

    # r.is_ok() => r
    # r.is_err() => not r
    # r.is_ok_and(f) => bool(r) and f(r.ok_value)
    # r.is_err_and(f) => not r and f(r.err_value)
    # r1.or_(r2) => r1 or r2
    # r.or_else(f) => r or f(r.value)
    # r1.and_(r2) => r1 and r2
    # r.and_then(f) => r.map_into(f)

    def is_ok_and(self, f: Predicate[T], /) -> bool: ...
    def is_err_and(self, f: Predicate[E], /) -> bool: ...
    def ok(self) -> "Option[T]": ...
    def err(self) -> "Option[E]": ...
    def map(self, f: abc.Callable[[T], U], /) -> "Result[U, E]": ...
    def map_into(
        self, f: abc.Callable[[T], "Result[U, F]"], /
    ) -> "Result[U, E] | Result[U, F]": ...
    def map_or(self, f: abc.Callable[[T], U], /, default: D) -> U | D: ...
    def map_or_else(self, f: abc.Callable[[T], U], /, default: Factory[D]) -> U | D: ...
    def map_err(self, f: abc.Callable[[E], F], /) -> "Result[T, F]": ...
    def map_err_into(
        self, f: abc.Callable[[E], "Result[U, F]"], /
    ) -> "Result[T, F] | Result[U, F]": ...
    def inspect(self, f: abc.Callable[[T], object], /) -> Self: ...
    def inspect_err(self, f: abc.Callable[[E], object], /) -> Self: ...
    def unwrap(self, msg: str = ...) -> T: ...
    def unwrap_err(self, msg: str = ...) -> E: ...
    def unwrap_or(self, default: D, /) -> T | D: ...
    def unwrap_or_else(self, f: Factory[D], /) -> T | D: ...
    def __iter__(self) -> abc.Iterator[T]: ...
    def __bool__(self) -> bool: ...


@final
@attrs.define
class Ok(_Result[T, Never]):
    ok_value: Final[T] = attrs.field()

    @override
    def is_ok_and(self, f: Predicate[T], /) -> bool:
        return f(self.ok_value)

    @override
    def is_err_and(self, f: Predicate[Never], /) -> bool:
        return False

    @override
    def ok(self) -> "Some[T]":
        from monads.option import Some

        return Some(self.ok_value)

    @override
    def err(self) -> "Null":
        from monads.option import Null

        return Null.null

    @override
    def map(self, f: abc.Callable[[T], U], /) -> "Ok[U]":
        return Ok(f(self.ok_value))

    @override
    def map_into(self, f: abc.Callable[[T], "Result[U, E]"], /) -> "Result[U, E]":
        return f(self.ok_value)

    @override
    def map_or(self, f: abc.Callable[[T], U], /, default: object) -> U:
        return f(self.ok_value)

    @override
    def map_or_else(self, f: abc.Callable[[T], U], /, default: Factory[object]) -> U:
        return f(self.ok_value)

    @override
    def map_err(self, f: abc.Callable[[Never], object], /) -> Self:
        return self

    @override
    def map_err_into(self, f: abc.Callable[[Never], "Result[object, object]"], /) -> Self:
        return self

    @override
    def inspect(self, f: abc.Callable[[T], object], /) -> Self:
        f(self.ok_value)
        return self

    @override
    def inspect_err(self, f: abc.Callable[[Never], object], /) -> Self:
        return self

    @override
    def unwrap(self, msg: str = "") -> T:
        return self.ok_value

    @override
    def unwrap_err(self, msg: str = "unwrap_err on Ok") -> Never:
        raise UnwrapError(msg) from None

    @override
    def unwrap_or(self, default: object, /) -> T:
        return self.ok_value

    @override
    def unwrap_or_else(self, f: Factory[object], /) -> T:
        return self.ok_value

    @override
    def __iter__(self) -> abc.Iterator[T]:
        yield self.ok_value

    @override
    def __bool__(self) -> Literal[True]:
        return True


@final
@attrs.define
class Err(_Result[Never, E]):
    err_value: Final[E] = attrs.field()

    @override
    def is_ok_and(self, f: Predicate[Never], /) -> bool:
        return False

    @override
    def is_err_and(self, f: Predicate[E], /) -> bool:
        return f(self.err_value)

    @override
    def ok(self) -> "Null":
        from monads.option import Null

        return Null.null

    @override
    def err(self) -> "Some[E]":
        from monads.option import Some

        return Some(self.err_value)

    @override
    def map(self, f: abc.Callable[[Never], object], /) -> Self:
        return self

    @override
    def map_into(self, f: abc.Callable[[Never], "Result[object, object]"], /) -> Self:
        return self

    @override
    def map_or(self, f: abc.Callable[[Never], object], /, default: D) -> D:
        return default

    @override
    def map_or_else(self, f: abc.Callable[[Never], object], /, default: Factory[D]) -> D:
        return default()

    @override
    def map_err(self, f: abc.Callable[[E], F], /) -> "Err[F]":
        return Err(f(self.err_value))

    @override
    def map_err_into(self, f: abc.Callable[[E], "Result[T, F]"], /) -> "Result[T, F]":
        return f(self.err_value)

    @override
    def inspect(self, f: abc.Callable[[Never], object], /) -> Self:
        return self

    @override
    def inspect_err(self, f: abc.Callable[[E], object], /) -> Self:
        f(self.err_value)
        return self

    @override
    def unwrap(self, msg: str = "unwrap on Err") -> Never:
        raise UnwrapError(msg)

    @override
    def unwrap_err(self, msg: str = "") -> E:
        return self.err_value

    @override
    def unwrap_or(self, default: D, /) -> D:
        return default

    @override
    def unwrap_or_else(self, f: Factory[D], /) -> D:
        return f()

    @override
    def __iter__(self) -> abc.Iterator[Never]:
        return
        yield

    @override
    def __bool__(self) -> Literal[False]:
        return False


Result: TypeAlias = Ok[T] | Err[E]


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
