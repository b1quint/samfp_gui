#!python

from codecs import open
from os import path

from setuptools import setup, find_packages

from samfp_gui.version import api, feature, bug

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SAM-FP: GUI',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='%d.%d.%d' % (api, feature, bug),

    description='Graphical User Interface to operate the SAM-FP instrument.',
    long_description=long_description,

    # The project's main homepage.
    url='https://b1quint.github.io/fp_tools',

    # Author details
    author='Bruno Quint',
    author_email='bquint@ctio.noao.edu',

    # Choose your license
    license='3-clause BSD License',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # package_dir={'': 'samfp'},
    # packages=find_packages(),
    packages=['samfp_gui'],
    package_dir={'samfp_gui': 'samfp_gui'},
    package_data={'samfp_gui': ['icons/*.png']},
    scripts=['scripts/samfp-gui', 'scripts/fp_sami'],
    zip_safe=False,

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=[
    #     'configparser',
    #     'numpy',
    #     'PyQt5'
    # ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'xjoin=samfp.xjoin:main',
    #         'mkcube=samfp.mkcube:main',
    #     ],
    # },
)
