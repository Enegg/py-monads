from collections import abc
from typing import ParamSpec, TypeAlias
from typing_extensions import TypeVar

T = TypeVar("T", covariant=True)  # noqa: PLC0105
U = TypeVar("U", infer_variance=True)
E = TypeVar("E", covariant=True)  # noqa: PLC0105
F = TypeVar("F", infer_variance=True)
D = TypeVar("D", infer_variance=True)
P = ParamSpec("P")
ExcT = TypeVar("ExcT", bound=BaseException, infer_variance=True)

Predicate: TypeAlias = abc.Callable[[T], bool]
Factory: TypeAlias = abc.Callable[[], T]
AsyncFactory: TypeAlias = abc.Callable[[], abc.Awaitable[T]]
AsyncCallable: TypeAlias = abc.Callable[P, abc.Awaitable[T]]
