"""Optional values.

Copyright (c) 2024-present Eneg
"""

from collections import abc
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    Generic,
    Literal,
    Never,
    Self,
    TypeVar,
    final,
    overload,
    override,
)

import attrs

from monads._types import Factory, Predicate, SupportsGe, SupportsGt, SupportsLe, SupportsLt
from monads.exceptions import UnwrapError

if TYPE_CHECKING:
    from monads.result import Err, Ok

__all__ = ("Null", "Option", "Some")

type Option[T] = Some[T] | Null[T]
T = TypeVar("T", covariant=True)
# for some reason pyright infers invariance for Some[T], so lets force it


@final
@attrs.frozen
class Some(Generic[T]):
    """Option variant with some value of type `T`."""

    value: Final[T] = attrs.field()

    def is_some_and(self, f: Predicate[T], /) -> bool:
        return f(self.value)

    def is_null_or(self, f: Predicate[T], /) -> bool:
        return f(self.value)

    def unwrap(self, msg: str = "") -> T:
        return self.value

    def unwrap_or(self, default: object, /) -> T:
        return self.value

    def unwrap_or_else(self, f: Factory[object], /) -> T:
        return self.value

    def map[U](self, f: abc.Callable[[T], U], /) -> "Some[U]":
        return Some(f(self.value))

    def map_into[U](self, f: abc.Callable[[T], Option[U]], /) -> Option[U]:
        return f(self.value)

    def map_or[U](self, f: abc.Callable[[T], U], /, default: object) -> U:
        return f(self.value)

    def map_or_else[U](self, f: abc.Callable[[T], U], /, default: Factory[object]) -> U:
        return f(self.value)

    def inspect(self, f: abc.Callable[[T], object], /) -> Self:
        f(self.value)
        return self

    def ok_or[E](self, err: E, /) -> "Ok[T, E]":
        from monads.result import Ok

        return Ok(self.value)

    def ok_or_else[E](self, err: Factory[E], /) -> "Ok[T, E]":
        from monads.result import Ok

        return Ok(self.value)

    @overload
    def xor(self, other: "Null[Any]", /) -> "Some[T]": ...
    @overload
    def xor(self, other: "Some[Any]", /) -> "Null[T]": ...

    def xor(self, other: Option[Any], /) -> Option[T]:
        if not other:
            return self

        return Null.null

    def flatten[O: Option[Any]](self: "Some[O]") -> O:
        return self.value

    def __iter__(self) -> abc.Iterator[T]:
        yield self.value

    def __bool__(self) -> Literal[True]:
        return True

    def __gt__[U](self: "Some[SupportsGt[U]]", other: Option[U], /) -> bool:
        return self.value > other.value if other else True

    def __ge__[U](self: "Some[SupportsGe[U]]", other: Option[U], /) -> bool:
        return self.value >= other.value if other else True

    def __lt__[U](self: "Some[SupportsLt[U]]", other: Option[U], /) -> bool:
        return self.value < other.value if other else False

    def __le__[U](self: "Some[SupportsLe[U]]", other: Option[U], /) -> bool:
        return self.value <= other.value if other else False


@final
class Null[T = Never]:
    """Option variant of no value."""

    __slots__ = ()
    null: Final["Null[Any]"]  # pyright: ignore[reportGeneralTypeIssues]
    """Instance of `Null`."""

    def __new__(cls) -> "Null[T]":
        return cls.null

    @override
    def __repr__(self) -> str:
        return "Null.null"

    def is_some_and(self, f: Predicate[T], /) -> Literal[False]:
        return False

    def is_null_or(self, f: Predicate[T], /) -> Literal[True]:
        return True

    def unwrap(self, msg: str = "unwrap on Null") -> Never:
        raise UnwrapError(msg)

    def unwrap_or[D](self, default: D, /) -> D:
        return default

    def unwrap_or_else[U](self, f: Factory[U], /) -> U:
        return f()

    def map[E](self, f: abc.Callable[[T], E], /) -> "Null[E]":
        return Null.null

    def map_into[E](self, f: abc.Callable[[T], Option[E]], /) -> "Null[E]":
        return Null.null

    def map_or[D](self, f: abc.Callable[[T], object], /, default: D) -> D:
        return default

    def map_or_else[D](self, f: abc.Callable[[T], object], /, default: Factory[D]) -> D:
        return default()

    def inspect(self, f: abc.Callable[[T], object], /) -> Self:
        return self

    def ok_or[E](self, err: E, /) -> "Err[E, T]":
        from monads.result import Err

        return Err(err)

    def ok_or_else[E](self, err: Factory[E], /) -> "Err[E, T]":
        from monads.result import Err

        return Err(err())

    @overload
    def xor[U](self, other: "Null[U]", /) -> "Null[U]": ...
    @overload
    def xor[U](self, other: Some[U], /) -> Some[U]: ...

    def xor[U](self, other: Option[U], /) -> Option[U]:
        return other

    def flatten[U](self: "Null[Option[U]]") -> "Null[U]":
        return Null.null

    def __iter__(self) -> abc.Iterator[Never]:
        return
        yield

    def __bool__(self) -> Literal[False]:
        return False

    def __gt__[U](self: "Null[SupportsGt[U]]", other: Option[U], /) -> bool:
        return False

    def __ge__[U](self: "Null[SupportsGe[U]]", other: Option[U], /) -> bool:
        return not other

    def __lt__[U](self: "Null[SupportsLt[U]]", other: Option[U], /) -> bool:
        return bool(other)

    def __le__[U](self: "Null[SupportsLe[U]]", other: Option[U], /) -> bool:
        return True


Null.null = object.__new__(Null)  # pyright: ignore[reportAttributeAccessIssue]

if False:
    from typing import Protocol

    from monads.result import Result

    def assert_assignable() -> None:
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
            def map[U](self, f: abc.Callable[[T], U], /) -> Option[U]: ...
            def map_into[U](self, f: abc.Callable[[T], Option[U]], /) -> Option[U]: ...
            def map_or[U, D](self, f: abc.Callable[[T], U], /, default: D) -> U | D: ...
            def map_or_else[U, D](
                self, f: abc.Callable[[T], U], /, default: Factory[D]
            ) -> U | D: ...
            def inspect(self, f: abc.Callable[[T], object], /) -> Self: ...
            def ok_or[E](self, err: E, /) -> Result[T, E]: ...
            def ok_or_else[E](self, err: Factory[E], /) -> Result[T, E]: ...
            def xor[U](self, other: Option[U], /) -> Option[T] | Option[U]: ...
            def flatten(self: Option[Option[T]]) -> Option[T]: ...
            def __iter__(self) -> abc.Iterator[T]: ...
            def __bool__(self) -> bool: ...

        # xor fails to assign. Too bad!
        _1: _Option[object] = Some(object)
        _2: _Option[object] = Null.null
