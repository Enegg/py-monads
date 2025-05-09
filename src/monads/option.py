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
# TODO: microsoft/pyright#10367
# pyright infers invariance for 3.12 TypeVars in dataclass-likes;
# using old syntax to force covariance
T = TypeVar("T", covariant=True)


@final
@attrs.frozen
class Some(Generic[T]):
    """Option variant with some value of type `T`."""

    value: Final[T] = attrs.field()

    if TYPE_CHECKING:
        def __init__(self, value: T, /) -> None: ...

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

    def map[U](self, f: abc.Callable[[T], U], /) -> "Null[U]":
        return Null.null

    def map_into[U](self, f: abc.Callable[[T], Option[U]], /) -> "Null[U]":
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

    def xor[O: Option[Any]](self, other: O, /) -> O:
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
