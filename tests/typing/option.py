from collections import abc
from typing import Protocol, Self

from monads import option
from monads._types import Factory, Predicate
from monads.result import Result


class _Option[T](Protocol):
    # o.is_some() => o
    # o.is_null() => not o
    # o1.or(o2) => o1 or o2
    # o.or_else(f) => o or f()
    # o1.and(o2) => o1 and o2
    # o.and_then(f) => o.map_into(f)

    def is_some_and(self, f: Predicate[T], /) -> bool: ...
    def is_null_or(self, f: Predicate[T], /) -> bool: ...
    def unwrap(self, msg: str = ...) -> T: ...
    def unwrap_or[D](self, default: D, /) -> T | D: ...
    def unwrap_or_else[D](self, f: Factory[D], /) -> T | D: ...
    # def map[U](self, f: abc.Callable[[T], U], /) -> "_Option[U]": ...
    # def map_into[U](self, f: abc.Callable[[T], "_Option[U]"], /) -> "_Option[U]": ...
    def map_or[U, D](self, f: abc.Callable[[T], U], /, default: D) -> U | D: ...
    def map_or_else[U, D](self, f: abc.Callable[[T], U], /, default: Factory[D]) -> U | D: ...
    def inspect(self, f: abc.Callable[[T], object], /) -> Self: ...
    def ok_or[E](self, err: E, /) -> Result[T, E]: ...
    def ok_or_else[E](self, err: Factory[E], /) -> Result[T, E]: ...
    # def xor[U](self, other: "_Option[U]", /) -> "_Option[T] | _Option[U]": ...
    # def flatten(self: "_Option[_Option[T]]") -> "_Option[T]": ...
    def __iter__(self) -> abc.Iterator[T]: ...
    def __bool__(self) -> bool: ...


class Foo: ...


class Bar:
    foo: option.Option[Foo]


class Baz:
    bar: option.Option[Bar]


def func(baz: option.Option[Baz]) -> None:
    _ = (
        baz.map_into(lambda baz: baz.bar)
        .map_into(lambda bar: bar.foo)
        .map_or(lambda foo: id(foo), 123)
    )
    _ = (
        [option.Some(123), option.Null[int]()][0]
        .map(lambda i: i.to_bytes(2, "big"))
        .map(lambda b: b.find(b"1"))
        .inspect(print)
    )
    _O1: _Option[object] = option.Some(object())
    _O2: _Option[object] = option.Null.null

    _1 = option.Some(123)
    _2 = option.Null.null
    _3 = _1 or _2
    _4 = _1 and _2
    _5 = _1.xor(_2)
    _6 = _1.xor(_1)
    _7 = _2.xor(_1)

    _8 = [option.Some(option.Some(123)), option.Null[option.Option[int]]()][0]
    _9 = _8.flatten()

    _10 = [option.Some(123), option.Some("123")][0]
    _10.map(lambda w: w.capitalize)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]

    _11 = [option.Some(123), option.Null[bytes]()][0]
    _12 = _11.xor(_1)
    _13 = _1.xor(_11)
    _14 = _11.xor(_2)
    _15 = _2.xor(_11)
    _16 = _11 or _1

    _ = _16 > _7
    _ = _6 < _3
    _ = _6 < _16
    _ = option.Some("123") > option.Some(123)  # pyright: ignore[reportUnknownVariableType, reportOperatorIssue]
    _ = _2.flatten()
