import datetime as py_datetime
from dataclasses import dataclass
from typing import Literal, Self, TypedDict

from ._duration import Duration
from ._time_zone import TimeZone

__all__ = ['PlainDate']


@dataclass(frozen = True)
class _PlainDateBase:
	py_date: py_datetime.date

	@classmethod
	def from_py_date(cls, py_date: py_datetime.date, /):
		return cls(py_date = py_date)


@dataclass(frozen = True)
class PlainDate(_PlainDateBase):

	def __init__(
		self,
		iso_year: int | None = None,
		iso_month: int | None = None,
		iso_day: int | None = None,
		/,
		calendar: Literal['iso8601'] = 'iso8601',
		*,
		py_date: py_datetime.date | None = None,
	):
		if py_date:
			super().__init__(py_date)
		else:
			assert iso_year
			assert iso_month
			assert iso_day
			super().__init__(py_datetime.date(iso_year, iso_month, iso_day))

	@classmethod
	def from_(
		cls,
		thing: 'PlainDate | str',
		/,
		*,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> Self:
		if isinstance(thing, PlainDate):
			return cls(py_date = thing.py_date.replace())
		# TODO parse
		return cls(py_date = py_datetime.date(2000, 1, 1))

	def with_(
		self,
		/,
		*,
		year: int | None = None,
		month: int | None = None,
		day: int | None = None,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> Self:
		# TODO other props
		return type(self)(
			year if year is not None else self.year,
			month if month is not None else self.month,
			day if day is not None else self.day,
		)

	@property
	def year(self, /) -> int:
		return self.py_date.year

	@property
	def month(self, /) -> int:
		return self.py_date.month

	@property
	def month_code(self, /) -> str:
		return f'M{self.py_date.month:02}'

	@property
	def day(self, /) -> int:
		return self.py_date.day

	@property
	def calendarId(self, /) -> str:
		return 'iso8601'

	@property
	def era(self, /) -> str | None:
		return None

	@property
	def era_year(self, /) -> str | None:
		return None

	@property
	def day_of_week(self, /) -> int:
		return self.py_date.isoweekday()

	@property
	def day_of_year(self, /) -> int:
		return (self.py_date - py_datetime.date(self.py_date.year, 1, 1)).days + 1

	@property
	def week_of_year(self, /) -> int:
		return self.py_date.isocalendar().week

	@property
	def year_of_week(self, /) -> int:
		return self.py_date.isocalendar().year

	@property
	def days_in_week(self, /) -> int:
		return 7

	@property
	def days_in_month(self, /) -> int:
		d = self.py_date
		while d.month == self.py_date.month:
			d += py_datetime.timedelta(days = 1)
		d -= py_datetime.timedelta(days = 1)
		return d.day

	@property
	def days_in_year(self, /) -> int:
		return (py_datetime.datetime(self.year, 12, 31) - py_datetime.datetime(self.year, 1, 1)).days + 1

	@property
	def months_in_year(self, /) -> int:
		return 12

	@property
	def in_leap_year(self, /) -> bool:
		return self.days_in_year == 366

	def add(
		self,
		duration: 'Duration | str',
		/,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> 'PlainDate':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def subtract(
		self,
		duration: 'Duration | str',
		/,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> 'PlainDate':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def until(
		self,
		other: 'Self | str',
		/,
		*,
		largest_unit: Literal['auto', 'year', 'month', 'week', 'day'] = 'auto',
		smallest_unit: Literal['year', 'month', 'week', 'day'] = 'day',
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
		largest_unit: Literal['auto', 'year', 'month', 'week', 'day'] = 'auto',
		smallest_unit: Literal['year', 'month', 'week', 'day'] = 'day',
		rounding_increment: int = 1,
		rounding_mode: Literal['ceil', 'floor', 'expand', 'trunc', 'halfCeil', 'halfFloor', 'halfExpand', 'halfTrunc', 'halfEven'] = 'trunc',
	) -> 'Duration':
		if not isinstance(other, type(self)):
			other = type(self).from_(other)
		# TODO
		return Duration()

	def to_string(self, /) -> str:
		# TODO
		return str(self)

	def to_locale_string(self) -> str:  # TODO options
		# TODO
		return str(self)

	def __str__(self):
		return self.py_date.isoformat()

	def __repr__(self):
		return f'{type(self).__name__}.from_("{self}")'

	def to_zoned_date_time(
		self,
		*,
		plain_time: 'PlainTime | str',
		time_zone: 'TimeZone',
	) -> '_zoned_date_time.ZonedDateTime':
		return _plain_date_time.PlainDateTime.to_zoned_date_time(
			None,  # type: ignore
			plain_date = self,
			plain_time = plain_time,
			time_zone = time_zone,
		)

	def to_plain_date_time(
		self,
		*,
		plain_time: 'PlainTime | str',
	) -> '_plain_date_time.PlainDateTime':
		return _plain_date_time.PlainDateTime.to_plain_date_time(
			None,  # type: ignore
			plain_date = self,
			plain_time = plain_time,
		)

	def to_plain_date(self) -> 'PlainDate':
		return PlainDate.from_py_date(self.py_date)

	class ISOFields(TypedDict):
		iso_year: int
		iso_month: int
		iso_day: int

	def get_iso_fields(self) -> ISOFields:
		return PlainDate.ISOFields(
			iso_year = self.year,
			iso_month = self.month,
			iso_day = self.day,
		)


from . import _plain_date_time, _zoned_date_time  # type: ignore
from ._plain_time import PlainTime
