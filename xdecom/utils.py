from typing import Any, BinaryIO, Collection, Iterator, Tuple, TypeVar, Union

T = TypeVar("T")


def noneif(val: T, noneish: Any) -> Union[T, None]:
    if val == noneish:
        val = None
    return val


def chunk_data(data: Collection[T], n: int) -> Iterator[Tuple[T, ...]]:
    "Collect data into fixed-length chunks or blocks"
    if len(data) % n != 0:
        raise ValueError(f"Cannot evenly divide {len(data)} items into chunks of {n} length.")
    for offset in range(0, len(data), n):
        yield(data[offset:offset + n])


def read_data(f: BinaryIO, start: int, end: int) -> bytes:
    """Read bytes from file in range [start, end)"""
    f.seek(start, 0)
    datalen = end - start
    data = f.read(datalen)
    return data
