# Non-Hashing Python Collections

As well all know, hash-based collections are a scourge upon the world (/s),
so this library contains implementations of common Python collections that would usually require hashability of its elements, but **without that requirement**.

## So... Why?

Python's `set`, `dict`, and a few other collections require their elements to be hashable, but sometimes types are not hashable.
Perhaps they could be, and even should be, but they aren't.
This library allows you use such types in typically hashed collections.

*Also* these implementations are natually insertion order preserving.
