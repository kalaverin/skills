---
source_hash: 82723fe3ee4de874
source_path: lib/pure/times.nim
---

# times

[ref: #module-times]

The times module contains routines and types for dealing with time using the [proleptic Gregorian calendar](https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar). It's also available for the [JavaScript target](backends.html#backends-the-javascript-target).

Although the times module supports nanosecond time resolution, the resolution used by getTime() depends on the platform and backend (JS is limited to millisecond precision).

# [Examples](#examples)

```
import std/[times, os]
# Simple benchmarking
let time = cpuTime()
sleep(100) # Replace this with something to be timed
echo "Time taken: ", cpuTime() - time

# Current date & time
let now1 = now()     # Current timestamp as a DateTime in local time
let now2 = now().utc # Current timestamp as a DateTime in UTC
let now3 = getTime() # Current timestamp as a Time

# Arithmetic using Duration
echo "One hour from now      : ", now() + initDuration(hours = 1)
# Arithmetic using TimeInterval
echo "One year from now      : ", now() + 1.years
echo "One month from now     : ", now() + 1.months
```

# [Parsing and Formatting Dates](#parsing-and-formatting-dates)

The DateTime type can be parsed and formatted using the different parse and format procedures.

```
let dt = parse("2000-01-01", "yyyy-MM-dd")
echo dt.format("yyyy-MM-dd")
```

The different format patterns that are supported are documented below.

| Pattern | Description | Example |
| --- | --- | --- |
| d | Numeric value representing the day of the month, it will be either one or two digits long. | 1/04/2012 -> 1 21/04/2012 -> 21 |
| dd | Same as above, but is always two digits. | 1/04/2012 -> 01 21/04/2012 -> 21 |
| ddd | Three letter string which indicates the day of the week. | Saturday -> Sat Monday -> Mon |
| dddd | Full string for the day of the week. | Saturday -> Saturday Monday -> Monday |
| GG | The last two digits of the Iso Week-Year | 30/12/2012 -> 13 |
| GGGG | The Iso week-calendar year padded to four digits | 30/12/2012 -> 2013 |
| h | The hours in one digit if possible. Ranging from 1-12. | 5pm -> 5 2am -> 2 |
| hh | The hours in two digits always. If the hour is one digit, 0 is prepended. | 5pm -> 05 11am -> 11 |
| H | The hours in one digit if possible, ranging from 0-23. | 5pm -> 17 2am -> 2 |
| HH | The hours in two digits always. 0 is prepended if the hour is one digit. | 5pm -> 17 2am -> 02 |
| m | The minutes in one digit if possible. | 5:30 -> 30 2:01 -> 1 |
| mm | Same as above but always two digits, 0 is prepended if the minute is one digit. | 5:30 -> 30 2:01 -> 01 |
| M | The month in one digit if possible. | September -> 9 December -> 12 |
| MM | The month in two digits always. 0 is prepended if the month value is one digit. | September -> 09 December -> 12 |
| MMM | Abbreviated three-letter form of the month. | September -> Sep December -> Dec |
| MMMM | Full month string, properly capitalized. | September -> September |
| s | Seconds as one digit if possible. | 00:00:06 -> 6 |
| ss | Same as above but always two digits. 0 is prepended if the second is one digit. | 00:00:06 -> 06 |
| t | A when time is in the AM. P when time is in the PM. | 5pm -> P 2am -> A |
| tt | Same as above, but AM and PM instead of A and P respectively. | 5pm -> PM 2am -> AM |
| yy | The last two digits of the year. When parsing, the current century is assumed. | 2012 AD -> 12 |
| yyyy | The year, padded to at least four digits. Is always positive, even when the year is BC. When the year is more than four digits, '+' is prepended. | 2012 AD -> 2012 24 AD -> 0024 24 BC -> 00024 12345 AD -> +12345 |
| YYYY | The year without any padding. Is always positive, even when the year is BC. | 2012 AD -> 2012 24 AD -> 24 24 BC -> 24 12345 AD -> 12345 |
| uuuu | The year, padded to at least four digits. Will be negative when the year is BC. When the year is more than four digits, '+' is prepended unless the year is BC. | 2012 AD -> 2012 24 AD -> 0024 24 BC -> -0023 12345 AD -> +12345 |
| UUUU | The year without any padding. Will be negative when the year is BC. | 2012 AD -> 2012 24 AD -> 24 24 BC -> -23 12345 AD -> 12345 |
| V | The Iso Week-Number as one or two digits | 3/2/2012 -> 5 1/4/2012 -> 13 |
| VV | The Iso Week-Number as two digits always. 0 is prepended if one digit. | 3/2/2012 -> 05 1/4/2012 -> 13 |
| z | Displays the timezone offset from UTC. | UTC+7 -> +7 UTC-5 -> -5 |
| zz | Same as above but with leading 0. | UTC+7 -> +07 UTC-5 -> -05 |
| zzz | Same as above but with :mm where *mm* represents minutes. | UTC+7 -> +07:00 UTC-5 -> -05:00 |
| ZZZ | Same as above but with mm where *mm* represents minutes. | UTC+7 -> +0700 UTC-5 -> -0500 |
| zzzz | Same as above but with :ss where *ss* represents seconds. | UTC+7 -> +07:00:00 UTC-5 -> -05:00:00 |
| ZZZZ | Same as above but with ss where *ss* represents seconds. | UTC+7 -> +070000 UTC-5 -> -050000 |
| g | Era: AD or BC | 300 AD -> AD 300 BC -> BC |
| fff | Milliseconds display | 1000000 nanoseconds -> 1 |
| ffffff | Microseconds display | 1000000 nanoseconds -> 1000 |
| fffffffff | Nanoseconds display | 1000000 nanoseconds -> 1000000 |

Other strings can be inserted by putting them in ''. For example hh'->'mm will give 01->56. In addition to spaces, the following characters can be inserted without quoting them: : - , . ( ) / [ ]. A literal ' can be specified with ''.

However you don't need to necessarily separate format patterns, as an unambiguous format string like yyyyMMddhhmmss is also valid (although only for years in the range 1..9999).

# [Duration vs TimeInterval](#duration-vs-timeinterval)

The times module exports two similar types that are both used to represent some amount of time: [Duration](#Duration) and [TimeInterval](#TimeInterval). This section explains how they differ and when one should be preferred over the other (short answer: use Duration unless support for months and years is needed).

## [Duration](#duration-vs-timeinterval-duration)

A Duration represents a duration of time stored as seconds and nanoseconds. A Duration is always fully normalized, so initDuration(hours = 1) and initDuration(minutes = 60) are equivalent.

Arithmetic with a Duration is very fast, especially when used with the Time type, since it only involves basic arithmetic. Because Duration is more performant and easier to understand it should generally preferred.

## [TimeInterval](#duration-vs-timeinterval-timeinterval)

A TimeInterval represents an amount of time expressed in calendar units, for example "1 year and 2 days". Since some units cannot be normalized (the length of a year is different for leap years for example), the TimeInterval type uses separate fields for every unit. The TimeInterval's returned from this module generally don't normalize **anything**, so even units that could be normalized (like seconds, milliseconds and so on) are left untouched.

Arithmetic with a TimeInterval can be very slow, because it requires timezone information.

Since it's slower and more complex, the TimeInterval type should be avoided unless the program explicitly needs the features it offers that Duration doesn't have.

## [How long is a day?](#duration-vs-timeinterval-how-long-is-a-dayqmark)

It should be especially noted that the handling of days differs between TimeInterval and Duration. The Duration type always treats a day as exactly 86400 seconds. For TimeInterval, it's more complex.

As an example, consider the amount of time between these two timestamps, both in the same timezone:

* 2018-03-25T12:00+02:00
* 2018-03-26T12:00+01:00

If only the date & time is considered, it appears that exactly one day has passed. However, the UTC offsets are different, which means that the UTC offset was changed somewhere in between. This happens twice each year for timezones that use daylight savings time. Because of this change, the amount of time that has passed is actually 25 hours.

The TimeInterval type uses calendar units, and will say that exactly one day has passed. The Duration type on the other hand normalizes everything to seconds, and will therefore say that 90000 seconds has passed, which is the same as 25 hours.

# [See also](#see-also)

* [monotimes module](monotimes.html)

## Examples

```nim
import std/[times, os]
# Simple benchmarking
let time = cpuTime()
sleep(100) # Replace this with something to be timed
echo "Time taken: ", cpuTime() - time

# Current date & time
let now1 = now()     # Current timestamp as a DateTime in local time
let now2 = now().utc # Current timestamp as a DateTime in UTC
let now3 = getTime() # Current timestamp as a Time

# Arithmetic using Duration
echo "One hour from now      : ", now() + initDuration(hours = 1)
# Arithmetic using TimeInterval
echo "One year from now      : ", now() + 1.years
echo "One month from now     : ", now() + 1.months
```

```nim
let dt = parse("2000-01-01", "yyyy-MM-dd")
echo dt.format("yyyy-MM-dd")
```

```nim
doAssert initDuration(seconds = 1) > DurationZero
doAssert initDuration(seconds = 0) == DurationZero
```

```nim
let dt = dateTime(2000, mJan, 01, 12, 00, 00, 00, utc())
doAssert $dt == "2000-01-01T12:00:00Z"
doAssert $default(DateTime) == "Uninitialized DateTime"
```

```nim
doAssert $initDuration(seconds = 2) == "2 seconds"
doAssert $initDuration(weeks = 1, days = 2) == "1 week and 2 days"
doAssert $initDuration(hours = 1, minutes = 2, seconds = 3) ==
  "1 hour, 2 minutes, and 3 seconds"
doAssert $initDuration(milliseconds = -1500) ==
  "-1 second and -500 milliseconds"
```

```nim
let f = initTimeFormat("yyyy-MM-dd")
doAssert $f == "yyyy-MM-dd"
```

```nim
doAssert $initTimeInterval(years = 1, nanoseconds = 123) ==
  "1 year and 123 nanoseconds"
doAssert $initTimeInterval() == "0 nanoseconds"
```

```nim
let dt = dateTime(1970, mJan, 01, 00, 00, 00, 00, local())
let tm = dt.toTime()
doAssert $tm == "1970-01-01T00:00:00" & format(dt, "zzz")
```

```nim
doAssert initDuration(seconds = 1) * 5 == initDuration(seconds = 5)
doAssert initDuration(minutes = 45) * 3 == initDuration(hours = 2, minutes = 15)
```

```nim
doAssert 5 * initDuration(seconds = 1) == initDuration(seconds = 5)
doAssert 3 * initDuration(minutes = 45) == initDuration(hours = 2, minutes = 15)
```

```nim
doAssert initDuration(seconds = 1) + initDuration(days = 1) ==
  initDuration(seconds = 1, days = 1)
```

```nim
doAssert (fromUnix(0) + initDuration(seconds = 1)) == fromUnix(1)
```

```nim
let dt = dateTime(2017, mMar, 30, 00, 00, 00, 00, utc())
let dur = initDuration(hours = 5)
doAssert $(dt + dur) == "2017-03-30T05:00:00Z"
```

```nim
let dt = dateTime(2017, mMar, 30, 00, 00, 00, 00, utc())
doAssert $(dt + 1.months) == "2017-04-30T00:00:00Z"
# This is correct and happens due to monthday overflow.
doAssert $(dt - 1.months) == "2017-03-02T00:00:00Z"
```

```nim
let tm = fromUnix(0)
doAssert tm + 5.seconds == fromUnix(5)
```

```nim
doAssert initDuration(seconds = 1, days = 1) - initDuration(seconds = 1) ==
  initDuration(days = 1)
```

```nim
doAssert initTime(1000, 100) - initTime(500, 20) ==
  initDuration(minutes = 8, seconds = 20, nanoseconds = 80)
```

```nim
doAssert -initDuration(seconds = 1) == initDuration(seconds = -1)
```

```nim
doAssert (fromUnix(0) - initDuration(seconds = 1)) == fromUnix(-1)
```

```nim
let dt1 = dateTime(2017, mMar, 30, 00, 00, 00, 00, utc())
let dt2 = dateTime(2017, mMar, 25, 00, 00, 00, 00, utc())

doAssert dt1 - dt2 == initDuration(days = 5)
```

```nim
let dt = dateTime(2017, mMar, 30, 00, 00, 00, 00, utc())
let dur = initDuration(days = 5)
doAssert $(dt - dur) == "2017-03-25T00:00:00Z"
```

```nim
let dt = dateTime(2017, mMar, 30, 00, 00, 00, 00, utc())
doAssert $(dt - 5.days) == "2017-03-25T00:00:00Z"
```

```nim
let ti1 = initTimeInterval(hours = 24)
let ti2 = initTimeInterval(hours = 4)
doAssert (ti1 - ti2) == initTimeInterval(hours = 20)
```

```nim
let day = -initTimeInterval(hours = 24)
doAssert day.hours == -24
```

```nim
let tm = fromUnix(5)
doAssert tm - 5.seconds == fromUnix(0)
```

```nim
doAssert initDuration(seconds = 1) < initDuration(seconds = 2)
doAssert initDuration(seconds = -2) < initDuration(seconds = 1)
doAssert initDuration(seconds = -2).abs < initDuration(seconds = 1).abs == false
```

```nim
doAssert initTime(50, 0) < initTime(99, 0)
```

```nim
let
  d1 = initDuration(weeks = 1)
  d2 = initDuration(days = 7)
doAssert d1 == d2
```

```nim
doAssert local() == local()
doAssert local() != utc()
```

```nim
doAssert initDuration(milliseconds = -1500).abs ==
  initDuration(milliseconds = 1500)
```

```nim
var a = dateTime(2015, mMar, 25, 12, 0, 0, 00, utc())
var b = dateTime(2017, mApr, 1, 15, 0, 15, 00, utc())
var ti = initTimeInterval(years = 2, weeks = 1, hours = 3, seconds = 15)
doAssert between(a, b) == ti
doAssert between(a, b) == -between(b, a)
```

```nim
doAssert convert(Days, Hours, 2) == 48
doAssert convert(Days, Weeks, 13) == 1 # Truncated
doAssert convert(Seconds, Milliseconds, -1) == -1000
```

```nim
var t0 = cpuTime()
# some useless work here (calculate fibonacci)
var fib = @[0, 1, 1]
for i in 1..10:
  fib.add(fib[^1] + fib[^2])
echo "CPU time [s] ", cpuTime() - t0
echo "Fib is [s] ", fib
```

```nim
assert $dateTime(2017, mMar, 30, zone = utc()) == "2017-03-30T00:00:00Z"
```

```nim
doAssert initDuration(seconds = 3) div 2 ==
  initDuration(milliseconds = 1500)
doAssert initDuration(minutes = 45) div 30 ==
  initDuration(minutes = 1, seconds = 30)
doAssert initDuration(nanoseconds = 3) div 2 ==
  initDuration(nanoseconds = 1)
```

```nim
let dt = dateTime(2000, mJan, 01, 00, 00, 00, 00, utc())
doAssert "2000-01-01" == format(dt, "yyyy-MM-dd")
```

```nim
let f = initTimeFormat("yyyy-MM-dd")
let dt = dateTime(2000, mJan, 01, 00, 00, 00, 00, utc())
doAssert "2000-01-01" == dt.format(f)
```

```nim
var dt = dateTime(1970, mJan, 01, 00, 00, 00, 00, utc())
var tm = dt.toTime()
doAssert format(tm, "yyyy-MM-dd'T'HH:mm:ss", utc()) == "1970-01-01T00:00:00"
```

```nim
doAssert $fromUnix(0).utc == "1970-01-01T00:00:00Z"
```

```nim
doAssert fromUnixFloat(123456.0) == fromUnixFloat(123456)
doAssert fromUnixFloat(-123456.0) == fromUnixFloat(-123456)
```

```nim
echo getClockStr(now() - 1.hours)
```

```nim
echo getDateStr(now() - 1.months)
```

```nim
doAssert getDayOfWeek(13, mJun, 1990) == dWed
doAssert $getDayOfWeek(13, mJun, 1990) == "Wednesday"
```

```nim
doAssert getDayOfYear(1, mJan, 2000) == 0
doAssert getDayOfYear(10, mJan, 2000) == 9
doAssert getDayOfYear(10, mFeb, 2000) == 40
```

```nim
doAssert getDaysInMonth(mFeb, 2000) == 29
doAssert getDaysInMonth(mFeb, 2001) == 28
```

```nim
doAssert getDaysInYear(2000) == 366
doAssert getDaysInYear(2001) == 365
```

```nim
assert getIsoWeekAndYear(initDateTime(21, mApr, 2018, 00, 00, 00)) == (isoweek: 16.IsoWeekRange, isoyear: 2018.IsoYear)
block:
  let (w, y) = getIsoWeekAndYear(initDateTime(30, mDec, 2019, 00, 00, 00))
  assert w == 01.IsoWeekRange
  assert y == 2020.IsoYear
assert getIsoWeekAndYear(initDateTime(13, mSep, 2020, 00, 00, 00)) == (isoweek: 37.IsoWeekRange, isoyear: 2020.IsoYear)
block:
  let (w, y) = getIsoWeekAndYear(initDateTime(2, mJan, 2021, 00, 00, 00))
  assert w.int > 52
  assert w.int < 54
  assert y.int mod 100 == 20
```

```nim
assert getWeeksInIsoYear(IsoYear(2019)) == 52
assert getWeeksInIsoYear(IsoYear(2020)) == 53
```

```nim
let dur = initDuration(hours = -50)
doAssert dur.inDays == -2
```

```nim
let dur = initDuration(minutes = 60, days = 2)
doAssert dur.inHours == 49
```

```nim
assert $initDateTime(30, mMar, 2017, 00, 00, 00, 00, utc()) == "2017-03-30T00:00:00Z"
```

```nim
assert $initDateTime(30, mMar, 2017, 00, 00, 00, utc()) == "2017-03-30T00:00:00Z"
```

```nim
let dur = initDuration(seconds = 1, milliseconds = 1)
doAssert dur.inMilliseconds == 1001
doAssert dur.inSeconds == 1
```

```nim
let f = initTimeFormat("yyyy-MM-dd")
doAssert "2000-01-01" == "2000-01-01".parse(f).format(f)
```

```nim
let day = initTimeInterval(hours = 24)
let dt = dateTime(2000, mJan, 01, 12, 00, 00, 00, utc())
doAssert $(dt + day) == "2000-01-02T12:00:00Z"
doAssert initTimeInterval(hours = 24) != initTimeInterval(days = 1)
```

```nim
let dur = initDuration(seconds = -2)
doAssert dur.inMicroseconds == -2000000
```

```nim
let dur = initDuration(seconds = -2)
doAssert dur.inMilliseconds == -2000
```

```nim
let dur = initDuration(hours = 2, seconds = 10)
doAssert dur.inMinutes == 120
```

```nim
let dur = initDuration(seconds = -2)
doAssert dur.inNanoseconds == -2000000000
```

```nim
let dur = initDuration(hours = 2, milliseconds = 10)
doAssert dur.inSeconds == 2 * 60 * 60
```

```nim
let dur = initDuration(days = 8)
doAssert dur.inWeeks == 1
```

```nim
doAssert now().isInitialized
doAssert not default(DateTime).isInitialized
```

```nim
let dt = dateTime(2020, mFeb, 29, 00, 00, 00, 00, utc())
doAssert dt.isLeapDay
doAssert dt+1.years-1.years != dt
let dt2 = dateTime(2020, mFeb, 28, 00, 00, 00, 00, utc())
doAssert not dt2.isLeapDay
doAssert dt2+1.years-1.years == dt2
doAssertRaises(Exception): discard dateTime(2021, mFeb, 29, 00, 00, 00, 00, utc())
```

```nim
doAssert isLeapYear(2000)
doAssert not isLeapYear(1900)
```

```nim
doAssert now().timezone == local()
doAssert local().name == "LOCAL"
```

```nim
proc utcTzInfo(time: Time): ZonedTime =
  ZonedTime(utcOffset: 0, isDst: false, time: time)
let utc = newTimezone("Etc/UTC", utcTzInfo, utcTzInfo)
```

```nim
let dt = dateTime(2000, mJan, 01, 00, 00, 00, 00, utc())
doAssert dt == parse("2000-01-01", "yyyy-MM-dd", utc())
```

```nim
let f = initTimeFormat("yyyy-MM-dd")
let dt = dateTime(2000, mJan, 01, 00, 00, 00, 00, utc())
doAssert dt == "2000-01-01".parse(f, utc())
```

```nim
let tStr = "1970-01-01T00:00:00+00:00"
doAssert parseTime(tStr, "yyyy-MM-dd'T'HH:mm:sszzz", utc()) == fromUnix(0)
```

```nim
var dp = toParts(initDuration(weeks = 2, days = 1))
doAssert dp[Days] == 1
doAssert dp[Weeks] == 2
doAssert dp[Minutes] == 0
dp = toParts(initDuration(days = -1))
doAssert dp[Days] == -1
```

```nim
var tp = toParts(initTimeInterval(years = 1, nanoseconds = 123))
doAssert tp[Years] == 1
doAssert tp[Nanoseconds] == 123
```

```nim
doAssert fromUnix(0).toUnix() == 0
```

```nim
let t = getTime()
# `<` because of rounding errors
doAssert abs(t.toUnixFloat().fromUnixFloat - t) < initDuration(nanoseconds = 1000)
```

```nim
doAssert now().utc.timezone == utc()
doAssert utc().name == "Etc/UTC"
```

## Const

### DefaultLocale

[ref: #symbol-defaultlocale]

```nim
DefaultLocale = (MMM: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                       "Sep", "Oct", "Nov", "Dec"], MMMM: ["January",
    "February", "March", "April", "May", "June", "July", "August", "September",
    "October", "November", "December"],
                 ddd: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], dddd: [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
```

### DurationZero

[ref: #symbol-durationzero]

Zero value for durations. Useful for comparisons.

```nim
DurationZero = (seconds: 0, nanosecond: 0)
```

Zero value for durations. Useful for comparisons.

```
doAssert initDuration(seconds = 1) > DurationZero
doAssert initDuration(seconds = 0) == DurationZero
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `p: IsoYear`

**Output:** `string`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `dur: Duration`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Human friendly string representation of a Duration.

### `$`

[ref: #symbol-]

**Input:**
- `zone: Timezone`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the name of the timezone.

### `$`

[ref: #symbol-]

**Input:**
- `f: TimeFormat`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the format string that was used to construct f.

### `$`

[ref: #symbol-]

**Input:**
- `dt: DateTime`

**Output:** `string`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Converts a DateTime object to a string representation. It uses the format yyyy-MM-dd'T'HH:mm:sszzz.

### `$`

[ref: #symbol-]

**Input:**
- `time: Time`

**Output:** `string`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Converts a Time value to a string representation. It will use the local time zone and use the format yyyy-MM-dd'T'HH:mm:sszzz.

### `$`

[ref: #symbol-]

**Input:**
- `ti: TimeInterval`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get string representation of TimeInterval.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `a: Duration`
- `b: Duration`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntLeDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `a: Time`
- `b: Time`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntLeTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a <= b.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `a: DateTime`
- `b: DateTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a happened before or at the same time as b.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `a: Duration`
- `b: Duration`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntLtDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Note that a duration can be negative, so even if a < b is true a might represent a larger absolute duration. Use abs(a) < abs(b) to compare the absolute duration.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `a: Time`
- `b: Time`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntLtTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a < b, that is if a happened before b.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `a: DateTime`
- `b: DateTime`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if a happened before b.

### `*=`

[ref: #symbol-]

**Input:**
- `a: var Duration`
- `b: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `a: int64`
- `b: Duration`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntMulInt64Duration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multiply a duration by some scalar.

### `*`

[ref: #symbol-]

**Input:**
- `a: Duration`
- `b: int64`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntMulDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multiply a duration by some scalar.

### `+=`

[ref: #symbol-]

**Input:**
- `d1: var Duration`
- `d2: Duration`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `t: var Time`
- `b: Duration`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `a: var DateTime`
- `b: Duration`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `a: var TimeInterval`
- `b: TimeInterval`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `a: var DateTime`
- `b: TimeInterval`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `t: var Time`
- `b: TimeInterval`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `a: Duration`
- `b: Duration`

**Output:** `Duration`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntAddDuration"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Add two durations together.

### `+`

[ref: #symbol-]

**Input:**
- `a: Time`
- `b: Duration`

**Output:** `Time`
**Pragmas:** `gcsafe`, `noSideEffect`, `gcsafe`, `extern: "ntAddTime"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Add a duration of time to a Time.

### `+`

[ref: #symbol-]

**Input:**
- `dt: DateTime`
- `dur: Duration`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `ti1: TimeInterval`
- `ti2: TimeInterval`

**Output:** `TimeInterval`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds two TimeInterval objects together.

### `+`

[ref: #symbol-]

Adds interval to dt. Components from interval are added in the order of their size, i.e. first the years component, then the months component and so on. The returned DateTime will have the same timezone as the input.

**Input:**
- `dt: DateTime`
- `interval: TimeInterval`

**Output:** `DateTime`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds interval to dt. Components from interval are added in the order of their size, i.e. first the years component, then the months component and so on. The returned DateTime will have the same timezone as the input.

Note that when adding months, monthday overflow is allowed. This means that if the resulting month doesn't have enough days it, the month will be incremented and the monthday will be set to the number of days overflowed. So adding one month to 31 October will result in 31 November, which will overflow and result in 1 December.

### `+`

[ref: #symbol-]

**Input:**
- `time: Time`
- `interval: TimeInterval`

**Output:** `Time`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds interval to time. If interval contains any years, months, weeks or days the operation is performed in the local timezone.


[Next](times_2.md)
