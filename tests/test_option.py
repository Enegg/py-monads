from monads import option


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
    _ = _2.flatten()
