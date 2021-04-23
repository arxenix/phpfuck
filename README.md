# phpfuck
Using only 5 different characters to write and execute arbitrary PHP.

```
(9^.)
```

Works in PHP7 only.

# How it works
- `9^99` -> `106`
  - use xor to generate numbers
- `(9).(9)` -> `'99'`
  - use `.` to concat numbers into strings
- `'09'^'1069'^'99'` -> `'80'`
  - xor 2 strings to get a string
- `'80'^0` -> `80`
  - (ab)use type juggling to cast a string to an int
- Using a combination of the above tricks, you can get all of the digits 0-9
- Can construct any number by concatenating digits and then casting to an int
- Constructing arbitrary strings requires a bit more work... 
  - the only primitive we have for obtaining strings is concat, which gives us a length-2 string
  - we can generate `/[a-z]{2,}/i` , but getting single-character strings is not possible
- `'funcname'(param)`
  - call functions by simply calling their string name
- `strtok(0)` -> `false`
  - call strtok on a number to get `false`
  - `=== ('st'+'rt'+'OK')(0)`
- `(9).false` -> `'9'`
  - concat number with `false` to get a length-1 string
- `'str'^'99'^'9'`
  - extract first char of any string with xor
- Can now build arbitrary strings `/[a-z]*/i`
- `'chr'(num)`
  - generate other characters (e.g. spaces)
- Can now build any string at all
- `str_getcsv("a,b")` -> `["a", "b"]`
  - create arrays by parsing a CSV
- `func(...["a", "b"])`
  - use spread operator to pass multiple arguments to a function
- `create_function("", "PAYLOAD")()`
  - use `create_function` to create a function w/ arbitrary PHP code and then call it
- Final payload looks like: `'create_function'(...str_getcsv(',"$PAYLOAD"'))`

# Todo
- compatibility with other PHP versions
  - the base string generation works across 4.3.0 - 8.0.3
  - function calls 'func'() do not work <= 7, they must be assigned to a variable first
  - anonymous functions also only in 7+
    - can do something like `call_user_func(...["assert","eval('echo 1; return 1;')"]);`
    - would only work for 5.6-7
  - ... spread operator only in 5.6+
  - `create_function` no longer in PHP8. don't know if there's any way to eval code so that we can use language constructs.
- generation website?
