# By value or by pointer?
This benchmark will show time of processing functions with arguments passed by value or pointer.

### Run
```sh
./run.sh
```
## Results
Example:

```
Build -O0
BENCH s1 by_value n=100000 t=0.13
BENCH s1 by_pointer n=100000 t=0.13

...

0Build -O1
...
0Build -O2
...
0Build -O3

```

Description:

`Build -O0` - what build option testing now

`BENCH s1 by_value n=100000 t=0.13`:

- `s1` - structure of 1 byte
- `n=100000` - number of tests,
- `t=0.13` average time by one test
