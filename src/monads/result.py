"""Error handling with the `Result` type.

Copyright (c) 2024-present Eneg
"""

from collections import abc
from typing import TYPE_CHECKING, Final, Literal, Never, Self, final

import attrs

from monads._types import Factory, Predicate
from monads.exceptions import UnwrapError

if TYPE_CHECKING:
    from monads.option import Null, Some

__all__ = ("Err", "Ok", "Result")

type Result[T, E] = Ok[T, E] | Err[E, T]


@final
@attrs.define
class Ok[T, E = Never]:
    ok_value: Final[T] = attrs.field()

    def is_ok_and(self, f: Predicate[T], /) -> bool:
        return f(self.ok_value)

    def is_err_and(self, f: Predicate[E], /) -> Literal[False]:
        return False

    def ok(self) -> "Some[T]":
        from monads.option import Some

        return Some(self.ok_value)

    def err(self) -> "Null[T]":
        from monads.option import Null

        return Null.null

    def map[U](self, f: abc.Callable[[T], U], /) -> "Ok[U, E]":
        return Ok(f(self.ok_value))

    def map_into[U, F](self, f: abc.Callable[[T], Result[U, F]], /) -> Result[U, F]:
        return f(self.ok_value)

    def map_or[U](self, f: abc.Callable[[T], U], /, default: object) -> U:
        return f(self.ok_value)

    def map_or_else[U](self, f: abc.Callable[[T], U], /, default: Factory[object]) -> U:
        return f(self.ok_value)

    def map_err[F](self, f: abc.Callable[[E], F], /) -> "Ok[T, F]":
        return Ok(self.ok_value)

    def map_err_into[U, F](self, f: abc.Callable[[E], Result[U, F]], /) -> "Ok[T, F]":
        return Ok(self.ok_value)

    def inspect(self, f: abc.Callable[[T], object], /) -> Self:
        f(self.ok_value)
        return self

    def inspect_err(self, f: abc.Callable[[E], object], /) -> Self:
        return self

    def unwrap(self, msg: str = "") -> T:
        return self.ok_value

    def unwrap_err(self, msg: str = "unwrap_err on Ok") -> Never:
        raise UnwrapError(msg) from None

    def unwrap_or(self, default: object, /) -> T:
        return self.ok_value

    def unwrap_or_else(self, f: Factory[object], /) -> T:
        return self.ok_value

    def __iter__(self) -> abc.Iterator[T]:
        yield self.ok_value

    def __bool__(self) -> Literal[True]:
        return True


@final
@attrs.define
class Err[E, T = Never]:
    err_value: Final[E] = attrs.field()

    def is_ok_and(self, f: Predicate[T], /) -> Literal[False]:
        return False

    def is_err_and(self, f: Predicate[E], /) -> bool:
        return f(self.err_value)

    def ok(self) -> "Null[E]":
        from monads.option import Null

        return Null.null

    def err(self) -> "Some[E]":
        from monads.option import Some

        return Some(self.err_value)

    def map[U](self, f: abc.Callable[[T], U], /) -> "Err[E, U]":
        return Err(self.err_value)

    def map_into[U, F](self, f: abc.Callable[[T], Result[U, F]], /) -> "Err[E, U]":
        return Err(self.err_value)

    def map_or[D](self, f: abc.Callable[[T], object], /, default: D) -> D:
        return default

    def map_or_else[D](self, f: abc.Callable[[T], object], /, default: Factory[D]) -> D:
        return default()

    def map_err[F](self, f: abc.Callable[[E], F], /) -> "Err[F, T]":
        return Err(f(self.err_value))

    def map_err_into[F, U](self, f: abc.Callable[[E], Result[F, U]], /) -> Result[F, U]:
        return f(self.err_value)

    def inspect(self, f: abc.Callable[[T], object], /) -> Self:
        return self

    def inspect_err(self, f: abc.Callable[[E], object], /) -> Self:
        f(self.err_value)
        return self

    def unwrap(self, msg: str = "unwrap on Err") -> Never:
        raise UnwrapError(msg)

    def unwrap_err(self, msg: str = "") -> E:
        return self.err_value

    def unwrap_or[D](self, default: D, /) -> D:
        return default

    def unwrap_or_else[D](self, f: Factory[D], /) -> D:
        return f()

    def __iter__(self) -> abc.Iterator[Never]:
        return
        yield

    def __bool__(self) -> Literal[False]:
        return False


if False:
    from typing import Protocol

    from monads.option import Option

    def assert_assignable() -> None:
        class _Result[T, E](Protocol):
            # r.is_ok() => r
            # r.is_err() => not r
            # r1.or(r2) => r1 or r2
            # r.or_else(f) => r or f(r.value)
            # r1.and(r2) => r1 and r2
            # r.and_then(f) => r.map_into(f)

            def is_ok_and(self, f: Predicate[T], /) -> bool: ...
            def is_err_and(self, f: Predicate[E], /) -> bool: ...
            def ok(self) -> Option[T]: ...
            def err(self) -> Option[E]: ...
            def map[U](self, f: abc.Callable[[T], U], /) -> Result[U, E]: ...
            def map_into[U, F](
                self, f: abc.Callable[[T], Result[U, F]], /
            ) -> Result[U, E] | Result[U, F]: ...
            def map_or[U, D](self, f: abc.Callable[[T], U], /, default: D) -> U | D: ...
            def map_or_else[U, D](
                self, f: abc.Callable[[T], U], /, default: Factory[D]
            ) -> U | D: ...
            def map_err[F](self, f: abc.Callable[[E], F], /) -> Result[T, F]: ...
            def map_err_into[U, F](
                self, f: abc.Callable[[E], Result[U, F]], /
            ) -> Result[T, F] | Result[U, F]: ...
            def inspect(self, f: abc.Callable[[T], object], /) -> Self: ...
            def inspect_err(self, f: abc.Callable[[E], object], /) -> Self: ...
            def unwrap(self, msg: str = ...) -> T: ...
            def unwrap_err(self, msg: str = ...) -> E: ...
            def unwrap_or[D](self, default: D, /) -> T | D: ...
            def unwrap_or_else[D](self, f: Factory[D], /) -> T | D: ...
            def __iter__(self) -> abc.Iterator[T]: ...
            def __bool__(self) -> bool: ...

        _1: _Result[object, Exception] = Ok[int, Exception](123)
        _2: _Result[object, Exception] = Err(RuntimeError())
