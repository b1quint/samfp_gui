---
layout: single
permalink: /docs/install/
title: "Installation"
author_profile: false
---

## Dependencies

I am just now updating from PyQt4 to PyQt5 since it seems to be the default when
 installing PyQt using the `conda install pyqt` command. Because of that, the
 requirements also changed a bit. Here is the known requirements:

- Python >= 2.6
- PyQt >= 5
- ConfigParser
- NumPy

I **strongly recommend** you to use [Anaconda](https://www.continuum.io/downloads) and the
[Astroconda Channel](https://astroconda.readthedocs.io/en/latest/)
since it is supposed to be an standard library and it was where this packaged
was developed on.


## Install

 Once downloaded, enter the folder that was created and type:

```bash
$ pip install -r requirements.txt
$ pip install .  
```

 If you are not a superuser you can either add the `--user`
flag so [PIP will install locally](https://pip.pypa.io/en/stable/reference/pip_install/#id43)
or you can use a
[Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
and installing it inside.

 If you are using [Astroconda](https://astroconda.readthedocs.io/en/latest/),
 you will have to fix the installation by typing

```bash
$ conda install nomkl
```

  [MKL](https://software.intel.com/en-us/mkl) is the Intel Math Kernel Libraty
    which is used by NumPy and SciPy and other Python libraries. This may
    cause their installation to crash under [Anaconda](https://www.continuum.io/downloads) Virtual Environments
    and that is why you may have to install a version that does not rely on it.
