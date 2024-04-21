import zoneinfo as py_zoneinfo
from dataclasses import dataclass
from typing import Literal, Self, Sequence

from ._instant import Instant

__all__ = ['TimeZone']


@dataclass(frozen = True)
class _TimeZoneBase:
	py_tzinfo: py_zoneinfo.ZoneInfo

	@classmethod
	def from_py_zoneinfo(cls, py_tzinfo: py_zoneinfo.ZoneInfo, /):
		return cls(py_tzinfo = py_tzinfo)

	@classmethod
	def from_(cls, thing: 'TimeZone | _zoned_date_time.ZonedDateTime | str') -> 'Self | TimeZone':
		if isinstance(thing, TimeZone):
			return thing
		if isinstance(thing, _zoned_date_time.ZonedDateTime):
			return cls(py_tzinfo = py_zoneinfo.ZoneInfo(thing.time_zone_id))
		# TODO parse
		return cls(py_tzinfo = py_zoneinfo.ZoneInfo('Europe/Warsaw'))


@dataclass(frozen = True)
class TimeZone(_TimeZoneBase):
	# TODO handle offset zones
	# TODO check __eq__ behavior

	def __init__(
		self,
		time_zone_identifier: str,
		/,
		*,
		py_tzinfo: py_zoneinfo.ZoneInfo | None = None,
	):
		super().__init__(py_tzinfo or py_zoneinfo.ZoneInfo(time_zone_identifier))

	@property
	def id(self):
		return self.py_tzinfo.key

	def get_offset_nanoseconds_for(self, instant: 'Instant | str', /) -> int:
		...

	def get_offset_string_for(self, instant: 'Instant | str', /) -> str:
		...

	def get_plain_date_time_for(self, instant: 'Instant | str', /) -> '_plain_date_time.PlainDateTime':
		...

	def get_instant_for(
		self,
		date_time: '_plain_date_time.PlainDateTime | str',
		/,
		*,
		disambiguation: Literal['compatible', 'earlier', 'later', 'reject'] = 'compatible',
	) -> 'Instant':
		...

	def get_possible_instants_for(self, date_time: '_plain_date_time.PlainDateTime | str', /) -> 'Sequence[Instant]':
		...

	def get_next_transition(self, starting_point: 'Instant | str') -> 'Instant | None':
		...

	def get_previous_transition(self, starting_point: 'Instant | str') -> 'Instant | None':
		...

	def __str__(self):
		return self.id

	def __repr__(self):
		return f'{type(self).__name__}.from_("{self}")'


from . import _plain_date_time, _zoned_date_time  # type: ignore
