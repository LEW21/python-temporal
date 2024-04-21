import datetime as py_datetime
from dataclasses import dataclass
from typing import Literal, Self

from ._duration import Duration
from ._plain_date import PlainDate
from ._plain_time import PlainTime
from ._time_zone import TimeZone

__all__ = ['PlainDateTime']


@dataclass(frozen = True)
class _PlainDateTimeBase:
	py_datetimenaive: py_datetime.datetime

	def __post_init__(self):
		assert self.py_datetimenaive.tzinfo is None

	@classmethod
	def from_py_datetimenaive(cls, py_datetimenaive: py_datetime.datetime):
		return cls(py_datetimenaive = py_datetimenaive)


@dataclass(frozen = True)
class PlainDateTime(_PlainDateTimeBase, PlainDate, PlainTime):

	@property
	def py_date(self) -> py_datetime.date:  # type: ignore
		return self.py_datetimenaive.date()

	@property
	def py_time(self) -> py_datetime.time:  # type: ignore
		return self.py_datetimenaive.time()

	def __init__(
		self,
		iso_year: int | None = None,
		iso_month: int | None = None,
		iso_day: int | None = None,
		iso_hour: int = 0,
		iso_minute: int = 0,
		iso_second: int = 0,
		iso_millisecond: int = 0,
		iso_microsecond: int = 0,
		iso_nanosecond: int = 0,
		/,
		calendar: Literal['iso8601'] = 'iso8601',
		*,
		py_datetimenaive: py_datetime.datetime | None = None,
	):
		if py_datetimenaive:
			super().__init__(py_datetimenaive)
		else:
			assert iso_year
			assert iso_month
			assert iso_day
			super().__init__(py_datetime.datetime(iso_year, iso_month, iso_day, iso_hour, iso_minute, iso_second, iso_millisecond * 1000 + iso_microsecond))

	@classmethod
	def from_(  # type: ignore
			cls,
			thing: 'PlainDateTime | str',
			/,
			*,
			overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> Self:
		if isinstance(thing, PlainDateTime):
			return cls(py_datetimenaive = thing.py_datetimenaive.replace())
		# TODO parse
		return cls(py_datetimenaive = py_datetime.datetime(2000, 1, 1))

	def with_(
		self,
		/,
		*,
		year: int | None = None,
		month: int | None = None,
		day: int | None = None,
		hour: int | None = None,
		minute: int | None = None,
		second: int | None = None,
		millisecond: int | None = None,
		microsecond: int | None = None,
		nanosecond: int | None = None,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> Self:
		# TODO other props
		return type(self)(
			year if year is not None else self.year,
			month if month is not None else self.month,
			day if day is not None else self.day,
			hour if hour is not None else self.hour,
			minute if minute is not None else self.minute,
			second if second is not None else self.second,
			millisecond if millisecond is not None else self.millisecond,
			microsecond if microsecond is not None else self.microsecond,
			nanosecond if nanosecond is not None else self.nanosecond,
		)

	def with_plain_time(self, plain_time: 'PlainTime | str', /):
		if isinstance(plain_time, str):
			plain_time = PlainTime.from_(plain_time)
		return type(self)(
			self.year,
			self.month,
			self.day,
			plain_time.hour,
			plain_time.minute,
			plain_time.second,
			plain_time.millisecond,
			plain_time.microsecond,
			plain_time.nanosecond,
		)

	def with_plain_date(self, plain_date: 'PlainDate | str', /):
		if isinstance(plain_date, str):
			plain_date = PlainDate.from_(plain_date)
		assert plain_date.calendarId == 'iso8601'
		return type(self)(
			plain_date.year,
			plain_date.month,
			plain_date.day,
			self.hour,
			self.minute,
			self.second,
			self.millisecond,
			self.microsecond,
			self.nanosecond,
			calendar = plain_date.calendarId,
		)

	def add(
		self,
		duration: 'Duration | str',
		/,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> 'PlainDateTime':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def subtract(
		self,
		duration: 'Duration | str',
		/,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> 'PlainDateTime':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def until(
		self,
		other: 'Self | str',
		/,
		*,
		largest_unit: Literal['auto', 'year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'auto',
		smallest_unit: Literal['year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'nanosecond',
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
		largest_unit: Literal['auto', 'year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'auto',
		smallest_unit: Literal['year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'] = 'nanosecond',
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
		smallest_unit: Literal['day', 'hour', 'minute', 'second', 'millisecond', 'microsecond', 'nanosecond'],
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
		return self.py_datetimenaive.isoformat()

	def __repr__(self):
		return f'{type(self).__name__}.from_("{self}")'

	def to_zoned_date_time(
		self,
		*,
		plain_date: 'PlainDate | str | None' = None,
		plain_time: 'PlainTime | str | None' = None,
		time_zone: 'TimeZone',
		disambiguation: Literal['compatible', 'earlier', 'later', 'reject'] = 'compatible',
	) -> '_zoned_date_time.ZonedDateTime':
		return _zoned_date_time.ZonedDateTime.to_zoned_date_time(
			None,  # type: ignore
			plain_date = plain_date or self,
			plain_time = plain_time or self,
			time_zone = time_zone,
			disambiguation = disambiguation,
		)

	def to_plain_date_time(
		self,
		*,
		plain_date: 'PlainDate | str | None' = None,
		plain_time: 'PlainTime | str | None' = None,
	) -> 'PlainDateTime':
		if isinstance(plain_date, str):
			plain_date = PlainDate.from_(plain_date)
		elif plain_date is None:
			plain_date = self
		if isinstance(plain_time, str):
			plain_time = PlainTime.from_(plain_time)
		elif plain_time is None:
			plain_time = self
		return PlainDateTime.from_py_datetimenaive(py_datetime.datetime.combine(plain_date.py_date, plain_time.py_time))

	class ISOFields(PlainDate.ISOFields, PlainTime.ISOFields):
		pass

	def get_iso_fields(self) -> ISOFields:
		return PlainDateTime.ISOFields(
			**PlainDate.get_iso_fields(self),
			**PlainTime.get_iso_fields(self),
		)


from . import _zoned_date_time  # type: ignore
