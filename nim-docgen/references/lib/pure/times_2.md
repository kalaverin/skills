---
source_hash: 82723fe3ee4de874
source_path: lib/pure/times.nim
---

### `-=`

[ref: #symbol-]

**Input:**
- `dt: var Duration`
- `ti: Duration`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `t: var Time`
- `b: Duration`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `a: var DateTime`
- `b: Duration`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `a: var TimeInterval`
- `b: TimeInterval`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `a: var DateTime`
- `b: TimeInterval`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `t: var Time`
- `b: TimeInterval`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `a: Duration`
- `b: Duration`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntSubDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Subtract a duration from another.

### `-`

[ref: #symbol-]

**Input:**
- `a: Duration`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntReverseDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reverse a duration.

### `-`

[ref: #symbol-]

**Input:**
- `a: Time`
- `b: Time`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntDiffTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the duration between two points in time.

### `-`

[ref: #symbol-]

**Input:**
- `a: Time`
- `b: Duration`

**Output:** `Time`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntSubTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Subtracts a duration of time from a Time.

### `-`

[ref: #symbol-]

**Input:**
- `dt: DateTime`
- `dur: Duration`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `dt1: DateTime`
- `dt2: DateTime`

**Output:** `Duration`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compute the duration between dt1 and dt2.

### `-`

[ref: #symbol-]

**Input:**
- `ti: TimeInterval`

**Output:** `TimeInterval`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reverses a time interval

### `-`

[ref: #symbol-]

Subtracts TimeInterval ti1 from ti2.

**Input:**
- `ti1: TimeInterval`
- `ti2: TimeInterval`

**Output:** `TimeInterval`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Subtracts TimeInterval ti1 from ti2.

Time components are subtracted one-by-one, see output:

### `-`

[ref: #symbol-]

**Input:**
- `dt: DateTime`
- `interval: TimeInterval`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Subtract interval from dt. Components from interval are subtracted in the order of their size, i.e. first the years component, then the months component and so on. The returned DateTime will have the same timezone as the input.

### `-`

[ref: #symbol-]

**Input:**
- `time: Time`
- `interval: TimeInterval`

**Output:** `Time`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Subtracts interval from Time time. If interval contains any years, months, weeks or days the operation is performed in the local timezone.

### `==`

[ref: #symbol-]

**Input:**
- `a: IsoYear`
- `b: IsoYear`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `a: Duration`
- `b: Duration`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntEqDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `a: Time`
- `b: Time`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntEqTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a == b, that is if both times represent the same point in time.

### `==`

[ref: #symbol-]

**Input:**
- `zone1: Timezone`
- `zone2: Timezone`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Two Timezone's are considered equal if their name is equal.

### `==`

[ref: #symbol-]

**Input:**
- `a: DateTime`
- `b: DateTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a and b represent the same point in time.

### `div`

[ref: #symbol-div]

**Input:**
- `a: Duration`
- `b: int64`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntDivDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Integer division for durations.

### abs

[ref: #symbol-abs]

**Input:**
- `a: Duration`

**Output:** `Duration`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### between

[ref: #symbol-between]

Gives the difference between startDt and endDt as a TimeInterval. The following guarantees about the result is given:

**Input:**
- `startDt: DateTime`
- `endDt: DateTime`

**Output:** `TimeInterval`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gives the difference between startDt and endDt as a TimeInterval. The following guarantees about the result is given:

* All fields will have the same sign.
* If startDt.timezone == endDt.timezone, it is guaranteed that startDt + between(startDt, endDt) == endDt.
* If startDt.timezone != endDt.timezone, then the result will be equivalent to between(startDt.utc, endDt.utc).

### convert

[ref: #symbol-convert]

**Input:**
- `unitFrom: FixedTimeUnit`
- `unitTo: FixedTimeUnit`
- `quantity: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Convert a quantity of some duration unit to another duration unit. This proc only deals with integers, so the result might be truncated.

### cpuTime

[ref: #symbol-cputime]

**Input:**
- *(none)*

**Output:** `float`
**Pragmas:** `tags: [TimeEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Gets time spent that the CPU spent to run the current process in seconds. This may be more useful for benchmarking than epochTime. However, it may measure the real time instead (depending on the OS). The value of the result has no meaning. To generate useful timing values, take the difference between the results of two cpuTime calls:

### dateTime

[ref: #symbol-datetime]

**Input:**
- `year: int`
- `month: Month`
- `monthday: MonthdayRange`
- `hour: HourRange = 0`
- `minute: MinuteRange = 0`
- `second: SecondRange = 0`
- `nanosecond: NanosecondRange = 0`
- `zone: Timezone = local()`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new [DateTime](#DateTime) in the specified timezone.

### days

[ref: #symbol-days]

TimeInterval of d days.

**Input:**
- `d: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of d days.

echo getTime() + 2.days

### epochTime

[ref: #symbol-epochtime]

Gets time after the UNIX epoch (1970) in seconds. It is a float because sub-second resolution is likely to be supported (depending on the hardware/OS).

**Input:**
- *(none)*

**Output:** `float`
**Pragmas:** `tags: [TimeEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Gets time after the UNIX epoch (1970) in seconds. It is a float because sub-second resolution is likely to be supported (depending on the hardware/OS).

getTime should generally be preferred over this proc.

**Warning:**
Unsuitable for benchmarking (but still better than now), use monotimes.getMonoTime or cpuTime instead, depending on the use case.

### format

[ref: #symbol-format]

**Input:**
- `dt: DateTime`
- `f: TimeFormat`
- `loc: DateTimeLocale = DefaultLocale`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Format dt using the format specified by f.

### format

[ref: #symbol-format]

Shorthand for constructing a TimeFormat and using it to format dt.

**Input:**
- `dt: DateTime`
- `f: string`
- `loc: DateTimeLocale = DefaultLocale`

**Output:** `string`
**Pragmas:** `raises: [TimeFormatParseError]`, `tags: []`, `forbids: []`

**Effects:** `raises: TimeFormatParseError`, `tags: `, `forbids: `

Shorthand for constructing a TimeFormat and using it to format dt.

See [Parsing and formatting dates](#parsing-and-formatting-dates) for documentation of the format argument.

### format

[ref: #symbol-format]

**Input:**
- `dt: DateTime`
- `f: static[string]`

**Output:** `string`
**Generic parameters:** `f:type`

**Pragmas:** `raises: []`

**Effects:** `raises: `

Overload that validates format at compile time.

### format

[ref: #symbol-format]

Shorthand for constructing a TimeFormat and using it to format time. Will use the timezone specified by zone.

**Input:**
- `time: Time`
- `f: string`
- `zone: Timezone = local()`

**Output:** `string`
**Pragmas:** `raises: [TimeFormatParseError]`, `tags: []`, `forbids: []`

**Effects:** `raises: TimeFormatParseError`, `tags: `, `forbids: `

Shorthand for constructing a TimeFormat and using it to format time. Will use the timezone specified by zone.

See [Parsing and formatting dates](#parsing-and-formatting-dates) for documentation of the f argument.

### format

[ref: #symbol-format]

**Input:**
- `time: Time`
- `f: static[string]`
- `zone: Timezone = local()`

**Output:** `string`
**Generic parameters:** `f:type`

**Pragmas:** `raises: []`

**Effects:** `raises: `

Overload that validates f at compile time.

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: DateTime | Time`
- `specifier: string`

**Output:** *(none)*
**Generic parameters:** `value:type`

adapter for strformat. Not intended to be called directly.

### fromUnix

[ref: #symbol-fromunix]

**Input:**
- `unix: int64`

**Output:** `Time`
**Pragmas:** `gcsafe`, `tags: []`, `raises: []`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Convert a unix timestamp (seconds since 1970-01-01T00:00:00Z) to a Time.

### fromWinTime

[ref: #symbol-fromwintime]

**Input:**
- `win: int64`

**Output:** `Time`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convert a Windows file time (100-nanosecond intervals since 1601-01-01T00:00:00Z) to a Time.

### getClockStr

[ref: #symbol-getclockstr]

**Input:**
- `dt:  = now()`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nt$1"`, `tags: [TimeEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Gets the current local clock time as a string of the format HH:mm:ss.

### getDateStr

[ref: #symbol-getdatestr]

**Input:**
- `dt:  = now()`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nt$1"`, `tags: [TimeEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Gets the current local date as a string of the format YYYY-MM-dd.

### getDayOfWeek

[ref: #symbol-getdayofweek]

**Input:**
- `monthday: MonthdayRange`
- `month: Month`
- `year: int`

**Output:** `WeekDay`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Returns the day of the week enum from day, month and year. Equivalent with dateTime(year, month, monthday, 0, 0, 0, 0).weekday.

### getDayOfYear

[ref: #symbol-getdayofyear]

**Input:**
- `monthday: MonthdayRange`
- `month: Month`
- `year: int`

**Output:** `YeardayRange`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Returns the day of the year. Equivalent with dateTime(year, month, monthday, 0, 0, 0, 0).yearday.

### getDaysInMonth

[ref: #symbol-getdaysinmonth]

**Input:**
- `month: Month`
- `year: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the number of days in month of year.

### getDaysInYear

[ref: #symbol-getdaysinyear]

**Input:**
- `year: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the number of days in a year

### getIsoWeekAndYear

[ref: #symbol-getisoweekandyear]

Returns the ISO 8601 week and year.

**Input:**
- `dt: DateTime`

**Output:** `tuple[isoweek: IsoWeekRange, isoyear: IsoYear]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the ISO 8601 week and year.

**Warning:**
The ISO week-based year can correspond to the following or previous year from 29 December to January 3.

### getTime

[ref: #symbol-gettime]

**Input:**
- *(none)*

**Output:** `Time`
**Pragmas:** `tags: [TimeEffect]`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Gets the current time as a Time with up to nanosecond resolution.

### getWeeksInIsoYear

[ref: #symbol-getweeksinisoyear]

**Input:**
- `y: IsoYear`

**Output:** `IsoWeekRange`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of weeks in the specified ISO 8601 week-based year, which can be either 53 or 52.

### high

[ref: #symbol-high]

**Input:**
- `typ: typedesc[Duration]`

**Output:** `Duration`
**Generic parameters:** `typ:type`

Get the longest representable duration.

### high

[ref: #symbol-high]

**Input:**
- `typ: typedesc[Time]`

**Output:** `Time`
**Generic parameters:** `typ:type`

### hour

[ref: #symbol-hour]

**Input:**
- `dt: DateTime`

**Output:** `HourRange`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of hours past midnight, in the range 0 to 23.

### hour=

[ref: #symbol-hour]

**Input:**
- `dt: var DateTime`
- `value: HourRange`

**Output:** *(none)*
**Pragmas:** `deprecated: "Deprecated since v1.3.1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hours

[ref: #symbol-hours]

TimeInterval of h hours.

**Input:**
- `h: int`

**Output:** `TimeInterval`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

TimeInterval of h hours.

echo getTime() + 2.hours

### inDays

[ref: #symbol-indays]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole days.

### inHours

[ref: #symbol-inhours]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole hours.

### initDateTime

[ref: #symbol-initdatetime]

**Input:**
- `monthday: MonthdayRange`
- `month: Month`
- `year: int`
- `hour: HourRange`
- `minute: MinuteRange`
- `second: SecondRange`
- `nanosecond: NanosecondRange`
- `zone: Timezone = local()`

**Output:** `DateTime`
**Pragmas:** `deprecated: "use `dateTime`"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new [DateTime](#DateTime) in the specified timezone.

### initDateTime

[ref: #symbol-initdatetime]

**Input:**
- `monthday: MonthdayRange`
- `month: Month`
- `year: int`
- `hour: HourRange`
- `minute: MinuteRange`
- `second: SecondRange`
- `zone: Timezone = local()`

**Output:** `DateTime`
**Pragmas:** `deprecated: "use `dateTime`"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new [DateTime](#DateTime) in the specified timezone.

### initDateTime

[ref: #symbol-initdatetime]

**Input:**
- `weekday: WeekDay`
- `isoweek: IsoWeekRange`
- `isoyear: IsoYear`
- `hour: HourRange`
- `minute: MinuteRange`
- `second: SecondRange`
- `nanosecond: NanosecondRange`
- `zone: Timezone = local()`

**Output:** `DateTime`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### initDateTime

[ref: #symbol-initdatetime]

**Input:**
- `weekday: WeekDay`
- `isoweek: IsoWeekRange`
- `isoyear: IsoYear`
- `hour: HourRange`
- `minute: MinuteRange`
- `second: SecondRange`
- `zone: Timezone = local()`

**Output:** `DateTime`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### initDuration

[ref: #symbol-initduration]

**Input:**
- `nanoseconds: int64 = 0`
- `microseconds: int64 = 0`
- `milliseconds: int64 = 0`
- `seconds: int64 = 0`
- `minutes: int64 = 0`
- `hours: int64 = 0`
- `days: int64 = 0`
- `weeks: int64 = 0`

**Output:** `Duration`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new [Duration](#Duration).

### initTime

[ref: #symbol-inittime]

**Input:**
- `unix: int64`
- `nanosecond: NanosecondRange`

**Output:** `Time`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a [Time](#Time) from a unix timestamp and a nanosecond part.

### initTimeFormat

[ref: #symbol-inittimeformat]

Construct a new time format for parsing & formatting time types.

**Input:**
- `format: string`

**Output:** `TimeFormat`
**Pragmas:** `raises: [TimeFormatParseError]`, `tags: []`, `forbids: []`

**Effects:** `raises: TimeFormatParseError`, `tags: `, `forbids: `

Construct a new time format for parsing & formatting time types.

See [Parsing and formatting dates](#parsing-and-formatting-dates) for documentation of the format argument.

### initTimeInterval

[ref: #symbol-inittimeinterval]

Creates a new [TimeInterval](#TimeInterval).

**Input:**
- `nanoseconds:  = 0`
- `microseconds:  = 0`
- `milliseconds:  = 0`
- `seconds:  = 0`
- `minutes:  = 0`
- `hours:  = 0`
- `days:  = 0`
- `weeks:  = 0`
- `months:  = 0`
- `years:  = 0`

**Output:** `TimeInterval`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new [TimeInterval](#TimeInterval).

This proc doesn't perform any normalization! For example, initTimeInterval(hours = 24) and initTimeInterval(days = 1) are not equal.

You can also use the convenience procedures called milliseconds, seconds, minutes, hours, days, months, and years.

### inMicroseconds

[ref: #symbol-inmicroseconds]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole microseconds.

### inMilliseconds

[ref: #symbol-inmilliseconds]

**Input:**
- `dur: Duration`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the duration to the number of whole milliseconds.


[Prev](times_1.md) | [Next](times_3.md)
