---
source_hash: 82723fe3ee4de874
source_path: lib/pure/times.nim
---

### HourRange

[ref: #symbol-hourrange]

```nim
HourRange = range[0 .. 23]
```

### IsoWeekRange

[ref: #symbol-isoweekrange]

```nim
IsoWeekRange = range[1 .. 53]
```

An ISO 8601 calendar week number.

### IsoYear

[ref: #symbol-isoyear]

An ISO 8601 calendar year number.

```nim
IsoYear = distinct int
```

An ISO 8601 calendar year number.

**Warning:**
The ISO week-based year can correspond to the following or previous year from 29 December to January 3.

### MinuteRange

[ref: #symbol-minuterange]

```nim
MinuteRange = range[0 .. 59]
```

### Month

[ref: #symbol-month]

```nim
Month = enum
  mJan = (1, "January"), mFeb = "February", mMar = "March", mApr = "April",
  mMay = "May", mJun = "June", mJul = "July", mAug = "August",
  mSep = "September", mOct = "October", mNov = "November", mDec = "December"
```

Represents a month. Note that the enum starts at 1, so ord(month) will give the month number in the range 1..12.

### MonthdayRange

[ref: #symbol-monthdayrange]

```nim
MonthdayRange = range[1 .. 31]
```

### NanosecondRange

[ref: #symbol-nanosecondrange]

```nim
NanosecondRange = range[0 .. 999999999]
```

### SecondRange

[ref: #symbol-secondrange]

```nim
SecondRange = range[0 .. 60]
```

Includes the value 60 to allow for a leap second. Note however that the second of a DateTime will never be a leap second.

### Time

[ref: #symbol-time]

```nim
Time = object
```

Represents a point in time.

### TimeFormat

[ref: #symbol-timeformat]

Represents a format for parsing and printing time types.

```nim
TimeFormat = object
```

Represents a format for parsing and printing time types.

To create a new TimeFormat use [initTimeFormat proc](#initTimeFormat,string).

### TimeFormatParseError

[ref: #symbol-timeformatparseerror]

```nim
TimeFormatParseError = object of ValueError
```

Raised when parsing a TimeFormat string fails.

### TimeInterval

[ref: #symbol-timeinterval]

Represents a non-fixed duration of time. Can be used to add and subtract non-fixed time units from a [DateTime](#DateTime) or [Time](#Time).

```nim
TimeInterval = object
  nanoseconds*: int          ## The number of nanoseconds
  microseconds*: int         ## The number of microseconds
  milliseconds*: int         ## The number of milliseconds
  seconds*: int              ## The number of seconds
  minutes*: int              ## The number of minutes
  hours*: int                ## The number of hours
  days*: int                 ## The number of days
  weeks*: int                ## The number of weeks
  months*: int               ## The number of months
  years*: int                ## The number of years
```

Represents a non-fixed duration of time. Can be used to add and subtract non-fixed time units from a [DateTime](#DateTime) or [Time](#Time).

Create a new TimeInterval with [initTimeInterval proc](#initTimeInterval,int,int,int,int,int,int,int,int,int,int).

Note that TimeInterval doesn't represent a fixed duration of time, since the duration of some units depend on the context (e.g a year can be either 365 or 366 days long). The non-fixed time units are years, months, days and week.

Note that TimeInterval's returned from the times module are never normalized. If you want to normalize a time unit, [Duration](#Duration) should be used instead.

### TimeIntervalParts

[ref: #symbol-timeintervalparts]

```nim
TimeIntervalParts = array[TimeUnit, int]
```

### TimeParseError

[ref: #symbol-timeparseerror]

```nim
TimeParseError = object of ValueError
```

Raised when parsing input using a TimeFormat fails.

### TimeUnit

[ref: #symbol-timeunit]

```nim
TimeUnit = enum
  Nanoseconds, Microseconds, Milliseconds, Seconds, Minutes, Hours, Days, Weeks,
  Months, Years
```

Different units of time.

### Timezone

[ref: #symbol-timezone]

```nim
Timezone = ref object
```

Timezone interface for supporting [DateTime](#DateTime)s of arbitrary timezones. The times module only supplies implementations for the system's local time and UTC.

### WeekDay

[ref: #symbol-weekday]

```nim
WeekDay = enum
  dMon = "Monday", dTue = "Tuesday", dWed = "Wednesday", dThu = "Thursday",
  dFri = "Friday", dSat = "Saturday", dSun = "Sunday"
```

Represents a weekday.

### YeardayRange

[ref: #symbol-yeardayrange]

```nim
YeardayRange = range[0 .. 365]
```

### ZonedTime

[ref: #symbol-zonedtime]

```nim
ZonedTime = object
  time*: Time                ## The point in time being represented.
  utcOffset*: int            ## The offset in seconds west of UTC,
                             ## including any offset due to DST.
  isDst*: bool               ## Determines whether DST is in effect.
```

Represents a point in time with an associated UTC offset and DST flag. This type is only used for implementing timezones.

[Prev](times_3.md)
