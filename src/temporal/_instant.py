import datetime as py_datetime
from dataclasses import dataclass
from typing import Literal, Self

from ._duration import Duration

__all__ = ['Instant']


@dataclass(frozen = True, order = True)
class _InstantBase:
	py_datetimeutc: py_datetime.datetime

	def __post_init__(self):
		assert self.py_datetimeutc.tzinfo is py_datetime.timezone.utc

	@classmethod
	def from_py_datetimeutc(cls, py_datetimeutc: py_datetime.datetime, /):
		return cls(py_datetimeutc = py_datetimeutc)


@dataclass(frozen = True)
class Instant(_InstantBase):

	def __init__(
		self,
		epoch_nanoseconds: int | None = None,
		/,
		*,
		py_datetimeutc: py_datetime.datetime | None = None,
	):
		if not py_datetimeutc:
			if epoch_nanoseconds is None:
				raise TypeError("Instant.__init__() missing 1 required positional argument: 'epoch_nanoseconds'")
			py_datetimeutc = py_datetime.datetime.fromtimestamp(epoch_nanoseconds // 1000000000, tz = py_datetime.timezone.utc)
			py_datetimeutc = py_datetimeutc.replace(microsecond = int(epoch_nanoseconds / 1000))
		super().__init__(py_datetimeutc)

	@classmethod
	def from_(cls, thing: 'Instant | str', /) -> Self:
		if isinstance(thing, Instant):
			return cls(py_datetimeutc = thing.py_datetimeutc.replace())
		# TODO parse
		val = py_datetime.datetime.fromisoformat(thing)
		return cls(py_datetimeutc = val.astimezone(py_datetime.timezone.utc))

	@classmethod
	def from_epoch_seconds(cls, epoch_seconds: int, /) -> Self:
		return cls(py_datetimeutc = py_datetime.datetime.fromtimestamp(epoch_seconds, py_datetime.timezone.utc))

	@classmethod
	def from_epoch_milliseconds(cls, epoch_milliseconds: int, /) -> Self:
		return cls(py_datetimeutc = py_datetime.datetime.fromtimestamp(epoch_milliseconds // 1000, py_datetime.timezone.utc).replace(microsecond = epoch_milliseconds * 1000))

	@classmethod
	def from_epoch_microseconds(cls, epoch_microseconds: int, /) -> Self:
		return cls(py_datetimeutc = py_datetime.datetime.fromtimestamp(epoch_microseconds // 1000000, py_datetime.timezone.utc).replace(microsecond = epoch_microseconds))

	@classmethod
	def from_epoch_nanoseconds(cls, epoch_nanoseconds: int, /) -> Self:
		return cls(py_datetimeutc = py_datetime.datetime.fromtimestamp(epoch_nanoseconds // 1000000000, py_datetime.timezone.utc).replace(microsecond = int(epoch_nanoseconds / 1000)))

	@property
	def epoch_seconds(self) -> int:
		return int(self.py_datetimeutc.timestamp())

	@property
	def epoch_milliseconds(self) -> int:
		return int(self.py_datetimeutc.timestamp() * 1000)

	@property
	def epoch_microseconds(self) -> int:
		return int(self.py_datetimeutc.timestamp() * 1000000)

	@property
	def epoch_nanoseconds(self) -> int:
		return int(self.py_datetimeutc.timestamp() * 1000000) * 1000

	def add(self, duration: 'Duration | str', /) -> 'Instant':
		if not isinstance(duration, Duration):
			duration = Duration.from_(duration)
		# TODO
		return self

	def subtract(self, duration: 'Duration | str', /) -> 'Instant':
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
		time_zone: '_time_zone.TimeZone | str',
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
		return self.py_datetimeutc.replace(tzinfo = None).isoformat() + 'Z'

	def __repr__(self):
		return f'{type(self).__name__}.from_("{self}")'

	def to_zoned_date_time_iso(
		self,
		time_zone: '_time_zone.TimeZone | str',
		/,
	) -> '_zoned_date_time.ZonedDateTime':
		if isinstance(time_zone, str):
			time_zone = _time_zone.TimeZone(time_zone)
		return _zoned_date_time.ZonedDateTime.from_py_datetimezoned(self.py_datetimeutc.astimezone(time_zone.py_tzinfo))

	def to_instant(self):
		return Instant.from_py_datetimeutc(self.py_datetimeutc)


from . import _time_zone, _zoned_date_time  # type: ignore
