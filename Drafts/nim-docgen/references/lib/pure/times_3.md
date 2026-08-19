---
source_hash: 82723fe3ee4de874
source_path: lib/pure/times.nim
---

### inMinutes

[ref: #symbol-inminutes]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole minutes.

### inNanoseconds

[ref: #symbol-innanoseconds]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole nanoseconds.

### inSeconds

[ref: #symbol-inseconds]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole seconds.

### inWeeks

[ref: #symbol-inweeks]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole weeks.

### inZone

[ref: #symbol-inzone]

**Input:**
- `time: Time`
- `zone: Timezone`

**Output:** `DateTime`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Convert time into a DateTime using zone as the timezone.

### inZone

[ref: #symbol-inzone]

**Input:**
- `dt: DateTime`
- `zone: Timezone`

**Output:** `DateTime`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Returns a DateTime representing the same point in time as dt but using zone as the timezone.

### isDst

[ref: #symbol-isdst]

**Input:**
- `dt: DateTime`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether DST is in effect. Always false for the JavaScript backend.

### isDst=

[ref: #symbol-isdst]

**Input:**
- `dt: var DateTime`
- `value: bool`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isLeapDay

[ref: #symbol-isleapday]

**Input:**
- `dt: DateTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns whether t is a leap day, i.e. Feb 29 in a leap year. This matters as it affects time offset calculations.

### isLeapYear

[ref: #symbol-isleapyear]

**Input:**
- `year: int`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if year is a leap year.

### local

[ref: #symbol-local]

**Input:**
- *(none)*

**Output:** `Timezone`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the Timezone implementation for the local timezone.

### local

[ref: #symbol-local]

**Input:**
- `dt: DateTime`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shorthand for dt.inZone(local()).

### local

[ref: #symbol-local]

**Input:**
- `t: Time`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shorthand for t.inZone(local()).

### low

[ref: #symbol-low]

**Input:**
- `typ: typedesc[Duration]`

**Output:** `Duration`
**Generic parameters:** `typ:type`

Get the longest representable duration of negative direction.

### low

[ref: #symbol-low]

**Input:**
- `typ: typedesc[Time]`

**Output:** `Time`
**Generic parameters:** `typ:type`

### microseconds

[ref: #symbol-microseconds]

**Input:**
- `micros: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of micros microseconds.

### milliseconds

[ref: #symbol-milliseconds]

**Input:**
- `ms: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of ms milliseconds.

### minute

[ref: #symbol-minute]

**Input:**
- `dt: DateTime`

**Output:** `MinuteRange`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of minutes after the hour, in the range 0 to 59.

### minute=

[ref: #symbol-minute]

**Input:**
- `dt: var DateTime`
- `value: MinuteRange`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### minutes

[ref: #symbol-minutes]

TimeInterval of m minutes.

**Input:**
- `m: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of m minutes.

echo getTime() + 5.minutes

### month

[ref: #symbol-month]

**Input:**
- `dt: DateTime`

**Output:** `Month`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The month as an enum, the ordinal value is in the range 1 to 12.

### monthday

[ref: #symbol-monthday]

**Input:**
- `dt: DateTime`

**Output:** `MonthdayRange`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The day of the month, in the range 1 to 31.

### monthdayZero=

[ref: #symbol-monthdayzero]

**Input:**
- `dt: var DateTime`
- `value: int`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### months

[ref: #symbol-months]

TimeInterval of m months.

**Input:**
- `m: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of m months.

echo getTime() + 2.months

### monthZero=

[ref: #symbol-monthzero]

**Input:**
- `dt: var DateTime`
- `value: int`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### name

[ref: #symbol-name]

The name of the timezone.

**Input:**
- `zone: Timezone`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The name of the timezone.

If possible, the name will be the name used in the tz database. If the timezone doesn't exist in the tz database, or if the timezone name is unknown, then any string that describes the timezone unambiguously might be used. For example, the string "LOCAL" is used for the system's local timezone.

See also: <https://en.wikipedia.org/wiki/Tz_database>

### nanosecond

[ref: #symbol-nanosecond]

**Input:**
- `time: Time`

**Output:** `NanosecondRange`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the fractional part of a Time as the number of nanoseconds of the second.

### nanosecond

[ref: #symbol-nanosecond]

**Input:**
- `dt: DateTime`

**Output:** `NanosecondRange`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of nanoseconds after the second, in the range 0 to 999\_999\_999.

### nanosecond=

[ref: #symbol-nanosecond]

**Input:**
- `dt: var DateTime`
- `value: NanosecondRange`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nanoseconds

[ref: #symbol-nanoseconds]

**Input:**
- `nanos: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of nanos nanoseconds.

### newTimezone

[ref: #symbol-newtimezone]

Create a new Timezone.

**Input:**
- `name: string`
- `zonedTimeFromTimeImpl: proc (time: Time): ZonedTime {.tags: [], raises: [], gcsafe.}`
- `zonedTimeFromAdjTimeImpl: proc (adjTime: Time): ZonedTime {.tags: [], raises: [], gcsafe.}`

**Output:** `owned Timezone`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new Timezone.

zonedTimeFromTimeImpl and zonedTimeFromAdjTimeImpl is used as the underlying implementations for zonedTimeFromTime and zonedTimeFromAdjTime.

If possible, the name parameter should match the name used in the tz database. If the timezone doesn't exist in the tz database, or if the timezone name is unknown, then any string that describes the timezone unambiguously can be used. Note that the timezones name is used for checking equality!

### now

[ref: #symbol-now]

Get the current time as a DateTime in the local timezone. Shorthand for getTime().local.

**Input:**
- *(none)*

**Output:** `DateTime`
**Pragmas:** `tags: [TimeEffect]`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Get the current time as a DateTime in the local timezone. Shorthand for getTime().local.

**Warning:**
Unsuitable for benchmarking, use monotimes.getMonoTime or cpuTime instead, depending on the use case.

### parse

[ref: #symbol-parse]

Parses input as a DateTime using the format specified by f. If no UTC offset was parsed, then input is assumed to be specified in the zone timezone. If a UTC offset was parsed, the result will be converted to the zone timezone.

**Input:**
- `input: string`
- `f: TimeFormat`
- `zone: Timezone = local()`
- `loc: DateTimeLocale = DefaultLocale`

**Output:** `DateTime`
**Pragmas:** `raises: [TimeParseError]`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: TimeParseError`, `tags: TimeEffect`, `forbids: `

Parses input as a DateTime using the format specified by f. If no UTC offset was parsed, then input is assumed to be specified in the zone timezone. If a UTC offset was parsed, the result will be converted to the zone timezone.

Month and day names from the passed in loc are used.

### parse

[ref: #symbol-parse]

Shorthand for constructing a TimeFormat and using it to parse input as a DateTime.

**Input:**
- `input: string`
- `f: string`
- `tz: Timezone = local()`
- `loc: DateTimeLocale = DefaultLocale`

**Output:** `DateTime`
**Pragmas:** `raises: [TimeParseError, TimeFormatParseError]`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: TimeParseError, TimeFormatParseError`, `tags: TimeEffect`, `forbids: `

Shorthand for constructing a TimeFormat and using it to parse input as a DateTime.

See [Parsing and formatting dates](#parsing-and-formatting-dates) for documentation of the f argument.

### parse

[ref: #symbol-parse]

**Input:**
- `input: string`
- `f: static[string]`
- `zone: Timezone = local()`
- `loc: DateTimeLocale = DefaultLocale`

**Output:** `DateTime`
**Generic parameters:** `f:type`

**Pragmas:** `raises: [TimeParseError]`

**Effects:** `raises: TimeParseError`

Overload that validates f at compile time.

### parseTime

[ref: #symbol-parsetime]

Shorthand for constructing a TimeFormat and using it to parse input as a DateTime, then converting it a Time.

**Input:**
- `input: string`
- `f: string`
- `zone: Timezone`

**Output:** `Time`
**Pragmas:** `raises: [TimeParseError, TimeFormatParseError]`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: TimeParseError, TimeFormatParseError`, `tags: TimeEffect`, `forbids: `

Shorthand for constructing a TimeFormat and using it to parse input as a DateTime, then converting it a Time.

See [Parsing and formatting dates](#parsing-and-formatting-dates) for documentation of the format argument.

### parseTime

[ref: #symbol-parsetime]

**Input:**
- `input: string`
- `f: static[string]`
- `zone: Timezone`

**Output:** `Time`
**Generic parameters:** `f:type`

**Pragmas:** `raises: [TimeParseError]`

**Effects:** `raises: TimeParseError`

Overload that validates format at compile time.

### second

[ref: #symbol-second]

**Input:**
- `dt: DateTime`

**Output:** `SecondRange`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of seconds after the minute, in the range 0 to 59.

### second=

[ref: #symbol-second]

**Input:**
- `dt: var DateTime`
- `value: SecondRange`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### seconds

[ref: #symbol-seconds]

TimeInterval of s seconds.

**Input:**
- `s: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of s seconds.

echo getTime() + 5.seconds

### timezone

[ref: #symbol-timezone]

**Input:**
- `dt: DateTime`

**Output:** `Timezone`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The timezone represented as an implementation of Timezone.

### timezone=

[ref: #symbol-timezone]

**Input:**
- `dt: var DateTime`
- `value: Timezone`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toParts

[ref: #symbol-toparts]

Converts a duration into an array consisting of fixed time units.

**Input:**
- `dur: Duration`

**Output:** `DurationParts`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a duration into an array consisting of fixed time units.

Each value in the array gives information about a specific unit of time, for example result[Days] gives a count of days.

This procedure is useful for converting Duration values to strings.

### toParts

[ref: #symbol-toparts]

Converts a TimeInterval into an array consisting of its time units, starting with nanoseconds and ending with years.

**Input:**
- `ti: TimeInterval`

**Output:** `TimeIntervalParts`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a TimeInterval into an array consisting of its time units, starting with nanoseconds and ending with years.

This procedure is useful for converting TimeInterval values to strings. E.g. then you need to implement custom interval printing

### toTime

[ref: #symbol-totime]

**Input:**
- `dt: DateTime`

**Output:** `Time`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Converts a DateTime to a Time representing the same point in time.

### toUnix

[ref: #symbol-tounix]

**Input:**
- `t: Time`

**Output:** `int64`
**Pragmas:** `gcsafe`, `tags: []`, `raises: []`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Convert t to a unix timestamp (seconds since 1970-01-01T00:00:00Z). See also toUnixFloat for subsecond resolution.

### toWinTime

[ref: #symbol-towintime]

**Input:**
- `t: Time`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convert t to a Windows file time (100-nanosecond intervals since 1601-01-01T00:00:00Z).

### utc

[ref: #symbol-utc]

**Input:**
- *(none)*

**Output:** `Timezone`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the Timezone implementation for the UTC timezone.

### utc

[ref: #symbol-utc]

**Input:**
- `dt: DateTime`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shorthand for dt.inZone(utc()).

### utc

[ref: #symbol-utc]

**Input:**
- `t: Time`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shorthand for t.inZone(utc()).

### utcOffset

[ref: #symbol-utcoffset]

**Input:**
- `dt: DateTime`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The offset in seconds west of UTC, including any offset due to DST. Note that the sign of this number is the opposite of the one in a formatted offset string like +01:00 (which would be equivalent to the UTC offset -3600).

### utcOffset=

[ref: #symbol-utcoffset]

**Input:**
- `dt: var DateTime`
- `value: int`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### weekday

[ref: #symbol-weekday]

**Input:**
- `dt: DateTime`

**Output:** `WeekDay`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The day of the week as an enum, the ordinal value is in the range 0 (monday) to 6 (sunday).

### weekday=

[ref: #symbol-weekday]

**Input:**
- `dt: var DateTime`
- `value: WeekDay`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### weeks

[ref: #symbol-weeks]

TimeInterval of w weeks.

**Input:**
- `w: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of w weeks.

echo getTime() + 2.weeks

### year

[ref: #symbol-year]

**Input:**
- `dt: DateTime`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The year, using astronomical year numbering (meaning that before year 1 is year 0, then year -1 and so on).

### year=

[ref: #symbol-year]

**Input:**
- `dt: var DateTime`
- `value: int`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### yearday

[ref: #symbol-yearday]

**Input:**
- `dt: DateTime`

**Output:** `YeardayRange`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of days since January 1, in the range 0 to 365.

### yearday=

[ref: #symbol-yearday]

**Input:**
- `dt: var DateTime`
- `value: YeardayRange`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### years

[ref: #symbol-years]

TimeInterval of y years.

**Input:**
- `y: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of y years.

echo getTime() + 2.years

### zonedTimeFromAdjTime

[ref: #symbol-zonedtimefromadjtime]

Returns the ZonedTime for some local time.

**Input:**
- `zone: Timezone`
- `adjTime: Time`

**Output:** `ZonedTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the ZonedTime for some local time.

Note that the Time argument does not represent a point in time, it represent a local time! E.g if adjTime is fromUnix(0), it should be interpreted as 1970-01-01T00:00:00 in the zone timezone, not in UTC.

### zonedTimeFromTime

[ref: #symbol-zonedtimefromtime]

**Input:**
- `zone: Timezone`
- `time: Time`

**Output:** `ZonedTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the ZonedTime for some point in time.

## Type

### DateTime

[ref: #symbol-datetime]

```nim
DateTime = object of RootObj
```

Represents a time in different parts. Although this type can represent leap seconds, they are generally not supported in this module. They are not ignored, but the DateTime's returned by procedures in this module will never have a leap second.

### DateTimeLocale

[ref: #symbol-datetimelocale]

```nim
DateTimeLocale = object
  MMM*: array[mJan .. mDec, string]
  MMMM*: array[mJan .. mDec, string]
  ddd*: array[dMon .. dSun, string]
  dddd*: array[dMon .. dSun, string]
```

### Duration

[ref: #symbol-duration]

Represents a fixed duration of time, meaning a duration that has constant length independent of the context.

```nim
Duration = object
```

Represents a fixed duration of time, meaning a duration that has constant length independent of the context.

To create a new Duration, use [initDuration](#initDuration,int64,int64,int64,int64,int64,int64,int64,int64). Instead of trying to access the private attributes, use [inSeconds](#inSeconds,Duration) for converting to seconds and [inNanoseconds](#inNanoseconds,Duration) for converting to nanoseconds.

### DurationParts

[ref: #symbol-durationparts]

```nim
DurationParts = array[FixedTimeUnit, int64]
```

### FixedTimeUnit

[ref: #symbol-fixedtimeunit]

```nim
FixedTimeUnit = range[Nanoseconds .. Weeks]
```

Subrange of TimeUnit that only includes units of fixed duration. These are the units that can be represented by a Duration.


[Prev](times_2.md) | [Next](times_4.md)
