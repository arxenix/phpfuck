# phpfuck
Using only 5 different characters to write and execute arbitrary PHP.

```
(9^.)
```

Works in PHP7 only.

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
