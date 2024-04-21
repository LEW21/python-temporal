from dataclasses import dataclass
from typing import Self


@dataclass
class Duration:
	...

	@classmethod
	def from_(cls, thing: 'Duration | str', /) -> Self:
		if isinstance(thing, Duration):
			return cls()
		# TODO parse
		return cls()
