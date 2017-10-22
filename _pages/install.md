---
layout: single
permalink: /docs/install/
title: "Install"
author_profile: false
---

We wrote `samfp-tools` in Python 2 but, in principle, it should be compatible
with Python 3. We simply did not have the chance yet to actually test the Py2
to Py3 conversion.

Since there are several ways which one can install a Python library, we decided
to develop `samfp` using the Virtual Environment
[Astroconda](https://astroconda.readthedocs.io/en/latest/) under [Anaconda](https://www.continuum.io/downloads). Once you have both installed
and running properly, activate the Astroconda Virtual Environment by typing

  ```bash
   source activate astroconda
  ```
  in a terminal.

After that, use `pip` to install `samfp` and its requirements:

  ```bash
  cd $path_to_samfp
  pip install -r requirements.txt
  pip install .
  ```
There is a know problem where both Numpy and SciPy fails to run under Anaconda because of a library called `mkl`. To fix that, type the following command

  ```bash
  conda install nomkl
  ```
After that, you should be able to run the SAM-FP Tools scripts from anywhere in your system, as long as you are the Virtual Environment where they were installed (e.g. Astroconda).
