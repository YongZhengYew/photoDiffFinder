# photoDiffFinder

A tool to draw bounding boxes around the differences between two different photos. Currently, there are 4 different methods of doing so, in Python files `method1.py`, `method2.py`, etc. This Git repository is mainly for testing these different methods on a predetermined set of testing data.

## How to Run

bash```
./tester.sh <-s> # include the -s option to save the resulting bounding boxes -- however, remember that saving may affect the timing results.
```

This will run all methods on each test case. The timing results will be saved in `results.txt` in the root directory. If you include the -s option, the bounding boxes will be saved in `testdir`, such as `testdir/1/2/METHOD1/XXX.png`. Keep in mind that re-running `./tester.sh -s` (with `-s` enabled) will overwrite the previous image results, so copy the entire `testdir` if you want to keep multiple results.

## Testing Data

We have 3 sets of data A B and C, which represent:
    A) Very simple images with one or two obvious changes
    B) Actual screenshots from a computer with minor changes (such as typing text in a word processor)
    C) Actual screenshots from a computer with major changes (such as scrolling a webpage or switching windows)
    
### File hierarchy
\_testdir
  \_1 -- Dataset A
    \_1 -- First pair of images in Dataset A
    \_2 -- etc.
    .
    .
    \_10
  \_2 -- Dataset B
    \_1
    \_2
    .
    .
    \_10
  \_3 -- Dataset C
     \_1
    \_2
    .
    .
    \_10

## Notes

An optimized version of Method 2 is currently in progress but is not in the testing script yet.
