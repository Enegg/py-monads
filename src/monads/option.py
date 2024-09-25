# pyright: reportImportCycles=false

from collections import abc
from enum import Enum
from typing import TYPE_CHECKING, Final, Literal, Protocol, TypeAlias, final, overload
from typing_extensions import Never, Self, override

import attrs

from monads.exceptions import UnwrapError
from monads.types import D, E, Factory, P, Predicate, T, U

if TYPE_CHECKING:
    from monads.result import Err, Ok, Result

else:
    from typing import Generic

__all__ = ("Null", "Option", "Some", "from_none", "try_option")


class _Option(Protocol[T]):
    __slots__ = ()

    # o.is_some() => o
    # o.is_null() => not o
    # o.is_some_and(f) => o and f(o.value)
    # o.is_none_or(f) => not o or f(o.value)
    # o1.or_(o2) => o1 or o2
    # o.or_else(f) => o or f()
    # o1.and_(o2) => o1 and o2
    # o.and_then(f) => o.map_into(f)

    def is_some_and(self, f: Predicate[T], /) -> bool: ...
    def is_null_or(self, f: Predicate[T], /) -> bool: ...
    def unwrap(self, msg: str = ...) -> T: ...
    def unwrap_or(self, default: D, /) -> T | D: ...
    def unwrap_or_else(self, f: Factory[D], /) -> T | D: ...
    def map(self, f: abc.Callable[[T], U], /) -> "Option[U]": ...
    def map_into(self, f: abc.Callable[[T], "Option[U]"], /) -> "Option[U]": ...
    def map_or(self, f: abc.Callable[[T], U], /, default: D) -> U | D: ...
    def map_or_else(self, f: abc.Callable[[T], U], /, default: Factory[D]) -> U | D: ...
    def inspect(self, f: abc.Callable[[T], object], /) -> Self: ...
    def ok_or(self, err: E, /) -> "Result[T, E]": ...
    def ok_or_else(self, err: Factory[E], /) -> "Result[T, E]": ...
    def xor(self, other: "Option[U]", /) -> "Self | Option[U]": ...
    def __iter__(self) -> abc.Iterator[T]: ...
    def __bool__(self) -> bool: ...


@final
@attrs.define
class Some(_Option[T]):
    value: Final[T] = attrs.field()

    @override
    def is_some_and(self, f: Predicate[T], /) -> bool:
        return f(self.value)

    @override
    def is_null_or(self, f: Predicate[T], /) -> bool:
        return f(self.value)

    @override
    def unwrap(self, msg: str = "") -> T:
        return self.value

    @override
    def unwrap_or(self, default: object, /) -> T:
        return self.value

    @override
    def unwrap_or_else(self, f: Factory[object], /) -> T:
        return self.value

    @override
    def map(self, f: abc.Callable[[T], U], /) -> "Some[U]":
        return Some(f(self.value))

    @override
    def map_into(self, f: abc.Callable[[T], "Option[U]"], /) -> "Option[U]":
        return f(self.value)

    @override
    def map_or(self, f: abc.Callable[[T], U], /, default: object) -> U:
        return f(self.value)

    @override
    def map_or_else(self, f: abc.Callable[[T], U], /, default: Factory[object]) -> U:
        return f(self.value)

    @override
    def inspect(self, f: abc.Callable[[T], object], /) -> Self:
        f(self.value)
        return self

    @override
    def ok_or(self, err: object, /) -> "Ok[T]":
        from monads.result import Ok

        return Ok(self.value)

    @override
    def ok_or_else(self, err: Factory[object], /) -> "Ok[T]":
        from monads.result import Ok

        return Ok(self.value)

    @overload
    def xor(self, other: "Null", /) -> Self: ...
    @overload
    def xor(self, other: "Some[object]", /) -> "Null": ...
    @override
    def xor(self, other: "Option[object]", /) -> "Option[T]":
        if other is Null.null:
            return self

        return Null.null

    @override
    def __iter__(self) -> abc.Iterator[T]:
        yield self.value

    @override
    def __bool__(self) -> Literal[True]:
        return True


@final
class Null(_Option[Never] if TYPE_CHECKING else Generic[T], Enum):
    # workaround for Protocol & Enum metaclass conflict
    __slots__ = ()
    null = None

    @override
    def is_some_and(self, f: Predicate[Never], /) -> bool:
        return False

    @override
    def is_null_or(self, f: Predicate[Never], /) -> bool:
        return True

    @override
    def unwrap(self, msg: str = "unwrap on Null") -> Never:
        raise UnwrapError(msg) from None

    @override
    def unwrap_or(self, default: D, /) -> D:
        return default

    @override
    def unwrap_or_else(self, f: Factory[U], /) -> U:
        return f()

    @override
    def map(self, f: abc.Callable[[Never], object], /) -> Self:
        return self

    @override
    def map_into(self, f: abc.Callable[[Never], "Option[object]"], /) -> Self:
        return self

    @override
    def map_or(self, f: abc.Callable[[Never], object], /, default: D) -> D:
        return default

    @override
    def map_or_else(self, f: abc.Callable[[Never], object], /, default: Factory[D]) -> D:
        return default()

    @override
    def inspect(self, f: abc.Callable[[Never], object], /) -> Self:
        return self

    @override
    def ok_or(self, err: E, /) -> "Err[E]":
        from monads.result import Err

        return Err(err)

    @override
    def ok_or_else(self, err: Factory[E], /) -> "Err[E]":
        from monads.result import Err

        return Err(err())

    @overload
    def xor(self, other: Self, /) -> Self: ...
    @overload
    def xor(self, other: Some[T], /) -> Some[T]: ...
    @override
    def xor(self, other: "Option[T]", /) -> "Option[T]":
        return other

    @override
    def __iter__(self) -> abc.Iterator[Never]:
        return
        yield

    @override
    def __bool__(self) -> Literal[False]:
        return False


Option: TypeAlias = Some[T] | Null


@overload
def from_none(obj: None, /) -> Null: ...
@overload
def from_none(obj: T | None, /) -> Option[T]: ...
def from_none(obj: T | None, /) -> Option[T]:
    """Turn `T | None` into `Option[T]`."""
    if obj is None:
        return Null.null

    return Some(obj)


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
