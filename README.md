# SAM-FP: Graphical User Interface

This package contains a graphical interface written using PyQt and Python 
to control the SAM-FP mode at the SOAR telescope. Be aware that it will only 
work if you are somehow inside SOAR's network since it uses TCP/IP to communicate
with the FP Plugin for SAMI, the SAM Imager. Please, follow up 
the instructions bellow to download and install your software.

Also, if the FP Plugin is not running on the SAMI's machine, this
program will not do anything actually. So you may want to connect 
to it via VNC and make sure it is running properly.

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

## Download it

 Since this software is under ocasional development, we stronhly recomend you
 to download one of the released versions. For that, you can use any of the link
 bellow:
 
- [samfp-gui.0.1.0.zip]()
- [samfp-gui.0.1.0.tar.gz]() 

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

## Run

Once you have it installed, the `samfp-gui` script will be accessible from 
anywhere in your terminal. Just open a new terminal and run it. 

## Feedback

Plase, your feedback is important for us. If you have any question
or any bug to report, use the 
[Issue Tracker ](https://github.com/b1quint/samfp_gui/issues)
on this page. 

## Contact

If you want a more personal approach you can write directly to me at
bquint at ctio dot noao dot edu.  