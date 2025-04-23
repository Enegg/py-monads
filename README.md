# monads

Python-flavored `Option[T]` and `Result[T, E]` types. Fully statically typed.

# features

### `monads.option`:
- `Option[T]` = `Some[T]` | `Null`
- support for `match` statement:
  ```py
  match option:
      case Some(value):
          print(value)

      case Null.Null:
          ...
  ```

### `monads.result`:
- `Result[T, E]` = `Ok[T]` | `Err[E]`
- support for `match` statement:
  ```py
  match result:
      case Ok(value):
          print(value)

      case Err(value):
          print(value)
  ```

### `monads.tools`:
- Turn `T | None` into `Option[T]` with `from_none`
- Turn exceptions into `Null` with `try_option`
- Turn functions that `return T` / `raise E` into `Result[T, E]` with `try_result`
- `CatchResult` context manager to turn arbitrary block of code into `Result`
