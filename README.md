# SAM-FP: Graphical User Interface

This package contains a graphical interface written using PyQt and Python 
to control the SAM-FP mode at the SOAR telescope. Be aware that it will only 
work if you are somehow inside SOAR's network since it uses TCP/IP to communicate
with the FP Plugin for SAMI, the SAM Imager. Please, follow up 
the instructions bellow to download and install your software.

Also, if the FP Plugin is not running on the SAMI's machine, this
program will not do anything actually. So you may want to connect 
to it via VNC and make sure it is running properly.

## Download

You can download it from a terminal by typing:

    $ git clone https://github.com/b1quint/samfp_gui.git

This is the ideal method for downloading this package since the GIT version-control 
protocol can be used to keep your version updated with ours. If you 
already have it, you can update your version with the command

    $ git pull 
    
from within the repository folder.

## Install 

Once downloaded, enter the folder that was created and type:

    $ pip install -r requirements.txt
    $ pip install . 
    
If you are not a superuser you can either add the `--user`
flag so [PIP will install locally](https://pip.pypa.io/en/stable/reference/pip_install/#id43) 
or you can use a 
[Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) 
and installing it inside. 

## Run

Once you have it installed, the `samfp-gui` script
will be accessible from anywhere in your terminal. Just
open a new terminal and run it. 

## Feedback

Plase, your feedback is important for us. If you have any question
or any bug to report, use the 
[Issue Tracker ](https://github.com/b1quint/samfp_gui/issues)
on this page. 

## Contact

If you want a more personal approach you can write directly to me at
bquint at ctio dot noao dot edu.  