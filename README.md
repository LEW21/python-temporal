# temporal
Python port of [JS Temporal proposal](https://tc39.es/proposal-temporal/docs/).

```sh
pip install temporal
```

```py
>>> from temporal import Now
>>> Now.zoned_date_time_iso()
ZonedDateTime.from_("2024-04-21T05:40:53.582028+02:00[Europe/Warsaw]")
```
