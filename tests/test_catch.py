from monads.tools import CatchResult


async def fetch(url: str) -> dict[str, object]: ...


async def main() -> None:
    with CatchResult(Exception) as catch:
        catch @= await fetch("lolz")  # noqa: PLW2901

    catch.result.map(lambda data: data)
