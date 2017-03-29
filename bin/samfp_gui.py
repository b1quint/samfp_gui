#/usr/bin/env python

from samfp_gui import gui, scan
from PyQt4 import QtGui

import sys

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    ex = gui.Main()
    sys.exit(app.exec_())