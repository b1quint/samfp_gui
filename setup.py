#/usr/bin/env python

from distutils.core import setup

setup(
    name='SAM-FP: GUI',
    version='0.0.1',
    description='Graphical User Interface to operate the SAM-FP instrument.',
    author='Bruno Quint',
    author_email='bquint@ctio.noao.edu',
    url='https://github.com/b1quint/samfp_gui',
    packages=['samfp_gui'],
    package_dir={'samfp_gui': 'samfp_gui'},
    package_data={'samfp_gui': ['icons/*.png']},
    scripts=['scripts/samfp-gui'],
    )