from monads import result


class Foo: ...


class Bar:
    foo: result.Result[Foo, Exception]


class Baz:
    bar: result.Result[Bar, TypeError]


def func(baz: result.Result[Baz, Exception]) -> None:
    _ = (
        baz.map_into(lambda baz: baz.bar)
        .map_into(lambda bar: bar.foo)
        .map_or(lambda foo: id(foo), 123)
    )

    _ = result.Ok(123)
