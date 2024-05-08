from collections.abc import MutableMapping
from typing import Iterable, Mapping, TypeVar, overload

K = TypeVar("K")
V = TypeVar("V")


class NonHashingDict(MutableMapping[K, V]):
    """Version of `dict` that supports non-hashable objects.

    Supporting non-hashable objects requires a less-optimal implementation;
    expect a decrease in performance.
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self: dict[str, V], **kwargs: V) -> None: ...

    @overload
    def __init__(self, map: Mapping[K, V], /) -> None: ...

    @overload
    def __init__(
        self: dict[str, V],
        map: Mapping[str, V],
        /,
        **kwargs: V,
    ) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[tuple[K, V]], /) -> None: ...

    @overload
    def __init__(
        self: dict[str, V],
        iterable: Iterable[tuple[str, V]],
        /,
        **kwargs: V,
    ) -> None: ...

    def __init__(
        self, obj: Mapping[K, V] | Iterable[tuple[K, V]] | None = None, /, **kwargs: V
    ) -> None:
        self._keys: list[K]
        self._values: list[V]
        if hasattr(obj, "keys"):
            self._keys = list(obj.keys())
            self._values = [obj[k] for k in self._keys]
        elif obj is None:
            self._keys = []
            self._values = []
        else:
            self._keys = []
            self._values = []
            for k, v in obj:
                self._keys.append(k)
                self._values.append(v)
        for k, v in kwargs.items():
            self._keys.append(k)
            self._values.append(v)

    def __iter__(self) -> Iterable[K]:
        return iter(self._keys)

    def __len__(self) -> int:
        return len(self._keys)

    def __getitem__(self, key: K, /) -> V:
        try:
            idx = self._keys.index(key)
        except ValueError:
            raise KeyError(repr(key)) from None
        else:
            return self._values[idx]

    def __setitem__(self, key: K, value: V, /) -> None:
        try:
            idx = self._keys.index(key)
        except ValueError:
            self._keys.append(key)
            self._values.append(value)
        else:
            self._values[idx] = value

    def __delitem__(self, key: K, /) -> None:
        try:
            idx = self._keys.index(key)
        except ValueError:
            raise KeyError(repr(key)) from None
        else:
            del self._keys[idx]
            del self._values[idx]

    def __repr__(self) -> str:
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"{type(self).__name__}([{items}])"
