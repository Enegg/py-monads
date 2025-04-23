from collections import abc
from typing import Protocol

type Predicate[T] = abc.Callable[[T], bool]
type Factory[T] = abc.Callable[[], T]


class SupportsLt[Rhs](Protocol):
    def __lt__(self, other: Rhs, /) -> bool: ...


class SupportsLe[Rhs](Protocol):
    def __le__(self, other: Rhs, /) -> bool: ...


class SupportsGt[Rhs](Protocol):
    def __gt__(self, other: Rhs, /) -> bool: ...


class SupportsGe[Rhs](Protocol):
    def __ge__(self, other: Rhs, /) -> bool: ...
