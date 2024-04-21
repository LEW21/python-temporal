import datetime as py_datetime
from dataclasses import dataclass
from typing import Literal, Self, TypedDict

from ._duration import Duration
from ._time_zone import TimeZone

__all__ = ['PlainTime']


@dataclass(frozen = True)
class _PlainTimeBase:
	py_time: py_datetime.time

	def __post_init__(self):
		assert self.py_time.tzinfo is None

	@classmethod
	def from_py_time(cls, py_time: py_datetime.time, /):
		return cls(py_time = py_time)


@dataclass(frozen = True)
class PlainTime(_PlainTimeBase):

	def __init__(
		self,
		iso_hour: int = 0,
		iso_minute: int = 0,
		iso_second: int = 0,
		iso_millisecond: int = 0,
		iso_microsecond: int = 0,
		iso_nanosecond: int = 0,
		/,
		*,
		py_time: py_datetime.time | None = None,
	):
		super().__init__(py_time or py_datetime.time(iso_hour, iso_minute, iso_second, iso_millisecond * 1000 + iso_microsecond))

	@classmethod
	def from_(
		cls,
		thing: 'PlainTime | str',
		/,
		*,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> Self:
		if isinstance(thing, PlainTime):
			return cls(py_time = thing.py_time.replace())
		# TODO parse
		return cls(py_time = py_datetime.time())

	def with_(
		self,
		/,
		*,
		hour: int | None = None,
		minute: int | None = None,
		second: int | None = None,
		millisecond: int | None = None,
		microsecond: int | None = None,
		nanosecond: int | None = None,
	) -> Self:
		return type(self)(
			hour if hour is not None else self.hour,
			minute if minute is not None else self.minute,
			second if second is not None else self.second,
			millisecond if millisecond is not None else self.millisecond,
			microsecond if microsecond is not None else self.microsecond,
			nanosecond if nanosecond is not None else self.nanosecond,
		)

	@property
	def hour(self, /) -> int:
		return self.py_time.hour

	@property
	def minute(self, /) -> int:
		return self.py_time.minute

	@property
	def second(self, /) -> int:
		return self.py_time.second

	@property
	def millisecond(self, /) -> int:
		return self.py_time.microsecond // 1000

	@property
	def microsecond(self, /) -> int:
		return self.py_time.microsecond % 1000

	@property
	def nanosecond(self, /) -> int:
		return 0

	def add(self, duration: 'Duration | str', /) -> 'PlainTime':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def subtract(self, duration: 'Duration | str', /) -> 'PlainTime':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def until(
		self,
		other: 'Self | str',
		/,
		*,
		largest_unit: Literal['auto', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'auto',
		smallest_unit: Literal['hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'nanosecond',
		rounding_increment: int = 1,
		rounding_mode: Literal['ceil', 'floor', 'expand', 'trunc', 'halfCeil', 'halfFloor', 'halfExpand', 'halfTrunc', 'halfEven'] = 'trunc',
	) -> 'Duration':
		if not isinstance(other, type(self)):
			other = type(self).from_(other)
		# TODO
		return Duration()

	def since(
		self,
		other: 'Self | str',
		/,
		*,
		largest_unit: Literal['auto', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'auto',
		smallest_unit: Literal['hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'nanosecond',
		rounding_increment: int = 1,
		rounding_mode: Literal['ceil', 'floor', 'expand', 'trunc', 'halfCeil', 'halfFloor', 'halfExpand', 'halfTrunc', 'halfEven'] = 'trunc',
	) -> 'Duration':
		if not isinstance(other, type(self)):
			other = type(self).from_(other)
		# TODO
		return Duration()

	def round(
		self,
		/,
		smallest_unit: Literal['hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'],
		*,
		rounding_increment: int = 1,
		rounding_mode: Literal['ceil', 'floor', 'expand', 'trunc', 'halfCeil', 'halfFloor', 'halfExpand', 'halfTrunc', 'halfEven'] = 'halfExpand',
	) -> Self:
		# TODO
		return self

	def to_string(
		self,
		/,
		*,
		fractional_second_digits: Literal['auto', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 'auto',
		smallest_unit: Literal['minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] | None = None,
		rounding_mode: Literal['ceil', 'floor', 'expand', 'trunc', 'halfCeil', 'halfFloor', 'halfExpand', 'halfTrunc', 'halfEven'] = 'trunc',
	) -> str:
		# TODO
		return str(self)

	def to_locale_string(self) -> str:  # TODO options
		# TODO
		return str(self)

	def __str__(self):
		return self.py_time.isoformat()

	def __repr__(self):
		return f'{type(self).__name__}.from_("{self}")'

	def to_zoned_date_time(
		self,
		*,
		plain_date: 'PlainDate | str',
		time_zone: 'TimeZone',
	) -> '_zoned_date_time.ZonedDateTime':
		return _plain_date_time.PlainDateTime.to_zoned_date_time(
			None,  # type: ignore
			plain_date = plain_date,
			plain_time = self,
			time_zone = time_zone,
		)

	def to_plain_date_time(
		self,
		*,
		plain_date: 'PlainDate | str',
	) -> '_plain_date_time.PlainDateTime':
		return _plain_date_time.PlainDateTime.to_plain_date_time(
			None,  # type: ignore
			plain_date = plain_date,
			plain_time = self,
		)

	def to_plain_time(self) -> 'PlainTime':
		return PlainTime.from_py_time(self.py_time)

	class ISOFields(TypedDict):
		iso_hour: int
		iso_minute: int
		iso_second: int
		iso_millisecond: int
		iso_microsecond: int
		iso_nanosecond: int

	def get_iso_fields(self) -> ISOFields:
		return PlainTime.ISOFields(
			iso_hour = self.hour,
			iso_minute = self.minute,
			iso_second = self.second,
			iso_millisecond = self.millisecond,
			iso_microsecond = self.microsecond,
			iso_nanosecond = self.nanosecond,
		)


from . import _plain_date_time, _zoned_date_time  # type: ignore
from ._plain_date import PlainDate
