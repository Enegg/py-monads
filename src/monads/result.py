"""Error handling with the `Result` type.

Copyright (c) 2024-present Eneg
"""

from collections import abc
from typing import TYPE_CHECKING, Final, Generic, Literal, Never, Self, TypeVar, final

import attrs

from monads._types import Factory, Predicate
from monads.exceptions import UnwrapError

if TYPE_CHECKING:
    from monads.option import Null, Some

__all__ = ("Err", "Ok", "Result")

type Result[T, E] = Ok[T, E] | Err[E, T]
OkT = TypeVar("OkT", covariant=True)
OkE = TypeVar("OkE", covariant=True, default=Never)
ErrE = TypeVar("ErrE", covariant=True)
ErrT = TypeVar("ErrT", covariant=True, default=Never)
# a bug in pyright infers invariance in dataclass-likes (likely due to __replace__),
# lets force covariance


@final
@attrs.frozen
class Ok(Generic[OkT, OkE]):
    ok_value: Final[OkT] = attrs.field()

    def is_ok_and(self, f: Predicate[OkT], /) -> bool:
        return f(self.ok_value)

    def is_err_and(self, f: Predicate[OkE], /) -> Literal[False]:
        return False

    def ok(self) -> "Some[OkT]":
        from monads.option import Some

        return Some(self.ok_value)

    def err(self) -> "Null[OkE]":
        from monads.option import Null

        return Null.null

    def map[U](self, f: abc.Callable[[OkT], U], /) -> "Ok[U, OkE]":
        return Ok(f(self.ok_value))

    def map_into[U, F](self, f: abc.Callable[[OkT], Result[U, F]], /) -> Result[U, F]:
        return f(self.ok_value)

    def map_or[U](self, f: abc.Callable[[OkT], U], /, default: object) -> U:
        return f(self.ok_value)

    def map_or_else[U](self, f: abc.Callable[[OkT], U], /, default: Factory[object]) -> U:
        return f(self.ok_value)

    def map_err[F](self, f: abc.Callable[[OkE], F], /) -> "Ok[OkT, F]":
        return Ok(self.ok_value)

    def map_err_into[U, F](self, f: abc.Callable[[OkE], Result[U, F]], /) -> "Ok[OkT, F]":
        return Ok(self.ok_value)

    def inspect(self, f: abc.Callable[[OkT], object], /) -> Self:
        f(self.ok_value)
        return self

    def inspect_err(self, f: abc.Callable[[OkE], object], /) -> Self:
        return self

    def unwrap(self, msg: str = "") -> OkT:
        return self.ok_value

    def unwrap_err(self, msg: str = "unwrap_err on Ok") -> Never:
        raise UnwrapError(msg)

    def unwrap_or(self, default: object, /) -> OkT:
        return self.ok_value

    def unwrap_or_else(self, f: Factory[object], /) -> OkT:
        return self.ok_value

    def __iter__(self) -> abc.Iterator[OkT]:
        yield self.ok_value

    def __bool__(self) -> Literal[True]:
        return True


@final
@attrs.frozen
class Err(Generic[ErrE, ErrT]):
    err_value: Final[ErrE] = attrs.field()

    def is_ok_and(self, f: Predicate[ErrT], /) -> Literal[False]:
        return False

    def is_err_and(self, f: Predicate[ErrE], /) -> bool:
        return f(self.err_value)

    def ok(self) -> "Null[ErrT]":
        from monads.option import Null

        return Null.null

    def err(self) -> "Some[ErrE]":
        from monads.option import Some

        return Some(self.err_value)

    def map[U](self, f: abc.Callable[[ErrT], U], /) -> "Err[ErrE, U]":
        return Err(self.err_value)

    def map_into[U, F](self, f: abc.Callable[[ErrT], Result[U, F]], /) -> "Err[ErrE, U]":
        return Err(self.err_value)

    def map_or[D](self, f: abc.Callable[[ErrT], object], /, default: D) -> D:
        return default

    def map_or_else[D](self, f: abc.Callable[[ErrT], object], /, default: Factory[D]) -> D:
        return default()

    def map_err[F](self, f: abc.Callable[[ErrE], F], /) -> "Err[F, ErrT]":
        return Err(f(self.err_value))

    def map_err_into[F, U](self, f: abc.Callable[[ErrE], Result[F, U]], /) -> Result[F, U]:
        return f(self.err_value)

    def inspect(self, f: abc.Callable[[ErrT], object], /) -> Self:
        return self

    def inspect_err(self, f: abc.Callable[[ErrE], object], /) -> Self:
        f(self.err_value)
        return self

    def unwrap(self, msg: str = "unwrap on Err") -> Never:
        raise UnwrapError(msg)

    def unwrap_err(self, msg: str = "") -> ErrE:
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
