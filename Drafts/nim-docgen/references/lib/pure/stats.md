---
source_hash: bd7e467322cb8c31
source_path: lib/pure/stats.nim
---

# stats

[ref: #module-stats]

Statistical analysis framework for performing basic statistical analysis of data. The data is analysed in a single pass, when it is pushed to a RunningStat or RunningRegress object.

RunningStat calculates for a single data set

* n (data count)
* min (smallest value)
* max (largest value)
* sum
* mean
* variance
* varianceS (sample variance)
* standardDeviation
* standardDeviationS (sample standard deviation)
* skewness (the third statistical moment)
* kurtosis (the fourth statistical moment)

RunningRegress calculates for two sets of data

* n (data count)
* slope
* intercept
* correlation

Procs are provided to calculate statistics on openArrays.

However, if more than a single statistical calculation is required, it is more efficient to push the data once to a RunningStat object and then call the numerous statistical procs for the RunningStat object:

## Examples

```nim
import std/stats
from std/math import almostEqual

template `~=`(a, b: float): bool = almostEqual(a, b)

var statistics: RunningStat  # must be var
statistics.push(@[1.0, 2.0, 1.0, 4.0, 1.0, 4.0, 1.0, 2.0])
doAssert statistics.n == 8
doAssert statistics.mean() ~= 2.0
doAssert statistics.variance() ~= 1.5
doAssert statistics.varianceS() ~= 1.714285714285715
doAssert statistics.skewness() ~= 0.8164965809277261
doAssert statistics.skewnessS() ~= 1.018350154434631
doAssert statistics.kurtosis() ~= -1.0
doAssert statistics.kurtosisS() ~= -0.7000000000000008
```

## Proc

### `$`

[ref: #symbol-]

Produces a string representation of the RunningStat. The exact format is currently unspecified and subject to change. Currently it contains:

**Input:**
- `a: RunningStat`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a string representation of the RunningStat. The exact format is currently unspecified and subject to change. Currently it contains:

* the number of probes
* min, max values
* sum, mean and standard deviation.

### `+=`

[ref: #symbol-]

**Input:**
- `a: var RunningStat`
- `b: RunningStat`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the RunningStat b to a.

### `+=`

[ref: #symbol-]

**Input:**
- `a: var RunningRegress`
- `b: RunningRegress`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the RunningRegress b to a.

### `+`

[ref: #symbol-]

Combines two RunningStats.

**Input:**
- `a: RunningStat`
- `b: RunningStat`

**Output:** `RunningStat`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Combines two RunningStats.

Useful when performing parallel analysis of data series and needing to re-combine parallel result sets.

### `+`

[ref: #symbol-]

Combines two RunningRegress objects.

**Input:**
- `a: RunningRegress`
- `b: RunningRegress`

**Output:** `RunningRegress`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Combines two RunningRegress objects.

Useful when performing parallel analysis of data series and needing to re-combine parallel result sets

### clear

[ref: #symbol-clear]

**Input:**
- `s: var RunningStat`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Resets s.

### clear

[ref: #symbol-clear]

**Input:**
- `r: var RunningRegress`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Resets r.

### correlation

[ref: #symbol-correlation]

**Input:**
- `r: RunningRegress`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current correlation of the two data sets pushed into r.

### intercept

[ref: #symbol-intercept]

**Input:**
- `r: RunningRegress`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current intercept of r.

### kurtosis

[ref: #symbol-kurtosis]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current population kurtosis of s.

### kurtosis

[ref: #symbol-kurtosis]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the population kurtosis of x.

### kurtosisS

[ref: #symbol-kurtosiss]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current sample kurtosis of s.

### kurtosisS

[ref: #symbol-kurtosiss]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the sample kurtosis of x.

### mean

[ref: #symbol-mean]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current mean of s.

### mean

[ref: #symbol-mean]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the mean of x.

### push

[ref: #symbol-push]

**Input:**
- `s: var RunningStat`
- `x: float`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Pushes a value x for processing.

### push

[ref: #symbol-push]

Pushes a value x for processing.

**Input:**
- `s: var RunningStat`
- `x: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Pushes a value x for processing.

x is simply converted to float and the other push operation is called.

### push

[ref: #symbol-push]

Pushes all values of x for processing.

**Input:**
- `s: var RunningStat`
- `x: openArray[float | int]`

**Output:** *(none)*
**Generic parameters:** `x:type`

Pushes all values of x for processing.

Int values of x are simply converted to float and the other push operation is called.

### push

[ref: #symbol-push]

**Input:**
- `r: var RunningRegress`
- `x: float`
- `y: float`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Pushes two values x and y for processing.

### push

[ref: #symbol-push]

Pushes two values x and y for processing.

**Input:**
- `r: var RunningRegress`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Pushes two values x and y for processing.

x and y are converted to float and the other push operation is called.

### push

[ref: #symbol-push]

**Input:**
- `r: var RunningRegress`
- `x: openArray[float | int]`
- `y: openArray[float | int]`

**Output:** *(none)*
**Generic parameters:** `x:type`

Pushes two sets of values x and y for processing.

### skewness

[ref: #symbol-skewness]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current population skewness of s.

### skewness

[ref: #symbol-skewness]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the population skewness of x.

### skewnessS

[ref: #symbol-skewnesss]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current sample skewness of s.

### skewnessS

[ref: #symbol-skewnesss]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the sample skewness of x.

### slope

[ref: #symbol-slope]

**Input:**
- `r: RunningRegress`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current slope of r.

### standardDeviation

[ref: #symbol-standarddeviation]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current population standard deviation of s.

### standardDeviation

[ref: #symbol-standarddeviation]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the population standard deviation of x.

### standardDeviationS

[ref: #symbol-standarddeviations]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current sample standard deviation of s.

### standardDeviationS

[ref: #symbol-standarddeviations]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the sample standard deviation of x.

### variance

[ref: #symbol-variance]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current population variance of s.

### variance

[ref: #symbol-variance]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the population variance of x.

### varianceS

[ref: #symbol-variances]

**Input:**
- `s: RunningStat`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the current sample variance of s.

### varianceS

[ref: #symbol-variances]

**Input:**
- `x: openArray[T]`

**Output:** `float`
**Generic parameters:** `T`

Computes the sample variance of x.

## Type

### RunningRegress

[ref: #symbol-runningregress]

```nim
RunningRegress = object
  n*: int                    ## amount of pushed data
  x_stats*: RunningStat      ## stats for the first set of data
  y_stats*: RunningStat      ## stats for the second set of data
```

An accumulator for regression calculations.

### RunningStat

[ref: #symbol-runningstat]

```nim
RunningStat = object
  n*: int                    ## amount of pushed data
  min*, max*, sum*: float    ## self-explaining
```

An accumulator for statistical data.
