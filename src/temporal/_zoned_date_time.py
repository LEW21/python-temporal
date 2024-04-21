import datetime as py_datetime
import zoneinfo as py_zoneinfo
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Self

from ._duration import Duration
from ._instant import Instant
from ._plain_date import PlainDate
from ._plain_date_time import PlainDateTime
from ._plain_time import PlainTime
from ._time_zone import TimeZone

__all__ = ['ZonedDateTime']


@dataclass(frozen = True)
class _ZonedDateTimeBase:
	py_datetimezoned: py_datetime.datetime

	def __post_init__(self):
		assert isinstance(self.py_datetimezoned.tzinfo, py_zoneinfo.ZoneInfo)

	@classmethod
	def from_py_datetimezoned(cls, py_datetimezoned: py_datetime.datetime):
		return cls(py_datetimezoned = py_datetimezoned)


@dataclass(frozen = True)
class ZonedDateTime(_ZonedDateTimeBase, PlainDateTime, Instant):

	@property
	def py_datetimenaive(self) -> py_datetime.datetime:  # type: ignore
		return self.py_datetimezoned.replace(tzinfo = None)

	@property
	def py_datetimeutc(self) -> py_datetime.datetime:  # type: ignore
		return self.py_datetimezoned.astimezone(py_datetime.timezone.utc)

	def __init__(
		self,
		epoch_nanoseconds: int | None = None,
		time_zone: 'TimeZone | None' = None,
		/,
		*,
		py_datetimezoned: py_datetime.datetime | None = None,
	):
		if not py_datetimezoned:
			if epoch_nanoseconds is None and time_zone is None:
				raise TypeError("ZonedDateTime.__init__() missing 2 required positional arguments: 'epoch_nanoseconds' and 'time_zone'")
			if epoch_nanoseconds is None:
				raise TypeError("ZonedDateTime.__init__() missing 1 required positional argument: 'epoch_nanoseconds'")
			if time_zone is None:
				raise TypeError("ZonedDateTime.__init__() missing 1 required positional argument: 'time_zone'")
			py_datetimezoned = py_datetime.datetime.fromtimestamp(epoch_nanoseconds / 1000000000, tz = time_zone.py_tzinfo)
			py_datetimezoned = py_datetimezoned.replace(microsecond = int(epoch_nanoseconds / 1000))
		super().__init__(py_datetimezoned)

	@classmethod
	def from_(  # type: ignore
			cls,
			thing: 'ZonedDateTime | str',
			/,
			*,
			overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> Self:
		if isinstance(thing, ZonedDateTime):
			return cls(py_datetimezoned = thing.py_datetimezoned.replace())
		# TODO parse
		return cls(py_datetimezoned = py_datetime.datetime(2000, 1, 1, tzinfo = py_zoneinfo.ZoneInfo('Europe/Warsaw')))

	# TODO with_, with_plain_time, with_plain_date

	@property
	def time_zone_id(self) -> str:
		assert isinstance(self.py_datetimezoned.tzinfo, py_zoneinfo.ZoneInfo)
		return self.py_datetimezoned.tzinfo.key

	def add(
		self,
		duration: 'Duration | str',
		/,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> 'ZonedDateTime':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def subtract(
		self,
		duration: 'Duration | str',
		/,
		overflow: Literal['constrain', 'reject'] = 'constrain',
	) -> 'ZonedDateTime':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def to_string(
		self,
		/,
		*,
		time_zone: 'TimeZone | str | None' = None,
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
		if TYPE_CHECKING:
			assert isinstance(self.py_datetimezoned.tzinfo, py_zoneinfo.ZoneInfo)
		return f"{self.py_datetimezoned.isoformat()}[{self.py_datetimezoned.tzinfo.key}]"

	def __repr__(self):
		return f'{type(self).__name__}.from_("{self}")'

	def to_zoned_date_time(
		self,
		*,
		plain_date: 'PlainDate | str | None' = None,
		plain_time: 'PlainTime | str | None' = None,
		time_zone: 'TimeZone | None' = None,
		disambiguation: Literal['compatible', 'earlier', 'later', 'reject'] = 'compatible',
	) -> 'ZonedDateTime':
		if isinstance(plain_date, str):
			plain_date = PlainDate.from_(plain_date)
		elif plain_date is None:
			plain_date = self
		if isinstance(plain_time, str):
			plain_time = PlainTime.from_(plain_time)
		elif plain_time is None:
			plain_time = self
		if time_zone is None:
			time_zone = TimeZone(self.time_zone_id)
		return ZonedDateTime.from_py_datetimezoned(py_datetime.datetime.combine(plain_date.py_date, plain_time.py_time, time_zone.py_tzinfo))

	class ISOFields(PlainDateTime.ISOFields):
		time_zone: TimeZone

	def get_iso_fields(self) -> ISOFields:
		return ZonedDateTime.ISOFields(
			**PlainDateTime.get_iso_fields(self),
			time_zone = TimeZone(self.time_zone_id),
		)
