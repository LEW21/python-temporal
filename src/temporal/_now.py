import datetime as py_datetime

from tzlocal import get_localzone_name

from ._instant import Instant
from ._plain_date import PlainDate
from ._plain_date_time import PlainDateTime
from ._plain_time import PlainTime
from ._time_zone import TimeZone
from ._zoned_date_time import ZonedDateTime

__all__ = ['Now']


class Now:

	@staticmethod
	def time_zone_id() -> str:
		return get_localzone_name()

	@staticmethod
	def instant() -> Instant:
		return Instant.from_py_datetimeutc(py_datetime.datetime.now(py_datetime.timezone.utc))

	@staticmethod
	def zoned_date_time_iso(time_zone: TimeZone | str | None = None, /) -> ZonedDateTime:
		if isinstance(time_zone, str):
			time_zone = TimeZone(time_zone)
		elif time_zone is None:
			time_zone = TimeZone(Now.time_zone_id())
		return ZonedDateTime.from_py_datetimezoned(py_datetime.datetime.now(time_zone.py_tzinfo))

	@staticmethod
	def plain_date_time_iso(time_zone: TimeZone | str | None = None, /) -> PlainDateTime:
		if isinstance(time_zone, str):
			time_zone = TimeZone(time_zone)
		return PlainDateTime.from_py_datetimenaive(py_datetime.datetime.now(time_zone.py_tzinfo if time_zone else None).replace(tzinfo = None))

	@staticmethod
	def plain_date_iso(time_zone: TimeZone | str | None = None, /) -> PlainDate:
		if isinstance(time_zone, str):
			time_zone = TimeZone(time_zone)
		return PlainDate.from_py_date(py_datetime.datetime.now(time_zone.py_tzinfo if time_zone else None).date())

	@staticmethod
	def plain_time_iso(time_zone: TimeZone | str | None = None, /) -> PlainTime:
		if isinstance(time_zone, str):
			time_zone = TimeZone(time_zone)
		return PlainTime.from_py_time(py_datetime.datetime.now(time_zone.py_tzinfo if time_zone else None).time())
