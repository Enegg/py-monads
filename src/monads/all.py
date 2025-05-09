"""Module exporting all public symbols.

Copyright (c) 2024-present Eneg
"""

from monads.exceptions import UnwrapError
from monads.option import Null, Option, Some
from monads.result import Err, Ok, Result
from monads.tools import (
    CatchResult,
    collect_options,
    collect_results,
    from_none,
    try_option,
    try_result,
)

__all__ = (
    "CatchResult",
    "Err",
    "Null",
    "Ok",
    "Option",
    "Result",
    "Some",
    "UnwrapError",
    "collect_options",
    "collect_results",
    "from_none",
    "try_option",
    "try_result",
)
