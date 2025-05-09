from collections import abc
from typing import Protocol, Self, reveal_type

from monads import option, result
from monads._types import Factory, Predicate
from monads.result import Err, Ok


class _Result[T, E](Protocol):
    # r.is_ok() => r
    # r.is_err() => not r
    # r1.or(r2) => r1 or r2
    # r.or_else(f) => r or f(r.value)
    # r1.and(r2) => r1 and r2
    # r.and_then(f) => r.map_into(f)

    def is_ok_and(self, f: Predicate[T], /) -> bool: ...
    def is_err_and(self, f: Predicate[E], /) -> bool: ...
    def ok(self) -> option.Option[T]: ...
    def err(self) -> option.Option[E]: ...
    def map[U](self, f: abc.Callable[[T], U], /) -> result.Result[U, E]: ...
    def map_into[U, F](
        self, f: abc.Callable[[T], result.Result[U, F]], /
    ) -> result.Result[U, E] | result.Result[U, F]: ...
    def map_or[U, D](self, f: abc.Callable[[T], U], /, default: D) -> U | D: ...
    def map_or_else[U, D](self, f: abc.Callable[[T], U], /, default: Factory[D]) -> U | D: ...
    def map_err[F](self, f: abc.Callable[[E], F], /) -> result.Result[T, F]: ...
    def map_err_into[U, F](
        self, f: abc.Callable[[E], result.Result[U, F]], /
    ) -> result.Result[T, F] | result.Result[U, F]: ...
    def inspect(self, f: abc.Callable[[T], object], /) -> Self: ...
    def inspect_err(self, f: abc.Callable[[E], object], /) -> Self: ...
    def unwrap(self, msg: str = ...) -> T: ...
    def unwrap_err(self, msg: str = ...) -> E: ...
    def unwrap_or[D](self, default: D, /) -> T | D: ...
    def unwrap_or_else[D](self, f: Factory[D], /) -> T | D: ...
    def __iter__(self) -> abc.Iterator[T]: ...
    def __bool__(self) -> bool: ...


class Foo: ...


class Bar:
    foo: result.Result[Foo, Exception]


class Baz:
    bar: result.Result[Bar, TypeError]


def func(baz: result.Result[Baz, Exception]) -> None:
    _ = (
        baz.inspect(lambda baz: reveal_type(baz.bar))
        .map_into(lambda baz: baz.bar)
        .map_into(lambda bar: bar.foo)
        .map_or(lambda foo: id(foo), 123)
    )

    _R1: _Result[object, Exception] = Ok[int, Exception](123)
    _R2: _Result[object, Exception] = Err(RuntimeError())
    _ = Ok(123) > Err("123")
    _ = Ok(123) > Ok("123")  # pyright: ignore[reportUnknownVariableType, reportOperatorIssue]
    _ = Err("123") >= Err(123)  # pyright: ignore[reportUnknownVariableType, reportOperatorIssue]
    _ = _R1 > _R1  # pyright: ignore[reportUnknownVariableType, reportOperatorIssue]
