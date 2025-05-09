# monads-py

Python-flavored `Option[T]` and `Result[T, E]`, empowered with static typing.

## features

### `monads.option`:
- `Option[T]` = `Some[T]` | `Null`
- support for `match` statement:
  ```py
  match option:
      case Some(value):
          print(value)

      case Null.null:
          ...
  ```

### `monads.result`:
- `Result[T, E]` = `Ok[T]` | `Err[E]`
- support for `match` statement:
  ```py
  match result:
      case Ok(value):
          print(value)

      case Err(err):
          print(err)
  ```

### `monads.tools`:
- `from_none` turns `T | None` into `Option[T]`:
  ```py
  data: dict[str, int] = {}
  value: Option[int] = from_none(data.get("foo"))
  ```
- `try_option` turns functions that `return T` or `raise E` into `Option[T]`
- `try_result` turns functions that `return T` or `raise E` into `Result[T, E]`
- `CatchResult` captures the result (or exception) of a block of code into `Result`:
  ```py
  with CatchResult(OSError) as catch:
      catch @= await client.get("foo")

  catch.result  # Ok(data) | Err(OSError(...))
  ```
- `collect_options` collects `Iterable[Option[T]]` into `Some[list[T]]` [iff][0] all options are `Some`, else `Null`
- `collect_results` collects `Iterable[Result[T, E]]` into `Ok[list[T]]` [iff][0] all results are `Ok`, else the first `Err[E]`

[0]: https://en.wikipedia.org/wiki/If_and_only_if "if and only if"