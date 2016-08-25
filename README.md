# BEASTCheck

A python tool for testing beast2 XML files.

[![Build Status](https://travis-ci.org/SimonGreenhill/beastcheck.svg?branch=master)](https://travis-ci.org/SimonGreenhill/beastcheck)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/beastcheck/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/beastcheck?branch=master)


## Usage:

Basic usage: 

###  Step 1. Create a test file called e.g. test.py
```python
import unittest
import beastcheck as b

class Analysis(b.BeastTest, unittest.TestCase):
    ntaxa = 10                      # Number of taxa
    nchar = 100                     # Number of sites
    ngenerations = 100000000        # Number of generations
    logEvery = 10000                # logging happens every ..
    filename = myfile.xml


if __name__ == '__main__':
    unittest.main()
```

NOTE: Every class that needs to run tests must subclass unittest.TestCase

### Step 2. Run:

```shell
python test.py
````

### Testing Multiple Files:

If you have a number of different analyses (say based on two different models) then you can set
up a parent class with the analysis particulars and subclass that for each xml file. 

```python
import unittest
import beastcheck as b

class Analysis(b.BeastTest):
    ntaxa = 10                      # Number of taxa
    nchar = 100                     # Number of sites
    ngenerations = 100000000        # Number of generations
    logEvery = 10000                # logging happens every ..


class TestAnalysis1(Analysis, unittest.TestCase):
    filename = myfile1.xml

class TestAnalysis2(Analysis, unittest.TestCase):
    ntaxa = 10
    nchar = 100
    filename = myfile2.xml


if __name__ == '__main__':
    unittest.main()
```



## Mixins:

Beastcheck has a number of mixins for testing different components of analyses, e.g. ModelCTMC adds test for the CTMC model.

To use, add them into your test case definition, e.g.:


```python
import unittest
import beastcheck as b

class Analysis(b.ModelCTMC, b.BeastTest, unittest.TestCase):
    ntaxa = 10                      # Number of taxa
    nchar = 100                     # Number of sites
    ngenerations = 100000000        # Number of generations
    logEvery = 10000                # logging happens every ..
````

### Clock Models:

* StrictClock
* RelaxedClock

### TreePriors:

* YuleTreePrior
* BayesianSkylineTreePrior
* BirthDeathSkylineSerialTreePrior

### Misc:

* AscertainmentBias
