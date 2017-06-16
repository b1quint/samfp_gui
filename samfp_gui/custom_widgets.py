from PyQt5 import QtCore, QtWidgets


class ComboBox(QtWidgets.QWidget):

    def __init__(self, label, options):

        super(ComboBox, self).__init__()

        self.label = QtWidgets.QLabel(label)
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(options)

    def __call__(self, x=None):

        if x is None:
            return str(self.combo_box.currentText())

        else:
            idx = self.combo_box.findText(x, QtCore.Qt.MatchFixedString)
            if idx >= 0:
                self.combo_box.setCurrentIndex(idx)


class TextTField(QtWidgets.QWidget):

    def __init__(self, label, value):
        """
        Initialize field that contains a label (QtWidgets.QLabel) and a text field
         (QtWidgets.QLineEdit).

        Parameters
        ----------
        label (string) : the field label
        text (string) : the text that will be inside the text box
        """
        super(TextTField, self).__init__()

        self.button = None
        self.label = QtWidgets.QLabel(label)
        self.line_edit = QtWidgets.QLineEdit(value)
        self.line_edit.setAlignment(QtCore.Qt.AlignRight)
        self._value = value

    def __call__(self, x=None):
        if x is None:
            x = self.line_edit.text()
            return x
        else:
            self.line_edit.setText(x)
            self._value = x

    def add_button(self, label):
        self.button = QtWidgets.QPushButton(label)

    def connect(self, method):

        if self.button is None:
            return

        self.button.clicked.connect(method)
        self.line_edit.returnPressed.connect(method)

    def disable(self):
        self.line_edit.setDisabled(True)

    def enable(self):
        self.line_edit.setEnabled(True)

    def set_field_max_width(self, p_int):
        self.line_edit.setMaximumWidth(p_int)

    def set_label(self, s):
        self.label.setText(s)


class IntTField(TextTField):

    def __init__(self, label, number):
        """
        Initialize field that contains a label (QtWidgets.QLabel) and a text field
         (QtWidgets.QLineEdit).

        Parameters
        ----------
        label (string) : the field label
        number (int) : the number that will be set to the field
        """
        assert (isinstance(number, int) or isinstance(number, float))
        number = int(number)

        super(IntTField, self).__init__(label, "{:d}".format(number))
        self._value = number

    def __call__(self, x=None):
        if x is None:
            x = self.line_edit.text()
            x = int(x)
            return x
        else:
            x = int(x)
            self.line_edit.setText("{:d}".format(x))
            self._value = x


class FloatTField(TextTField):

    def __init__(self, label, number):
        """
        Initialize field that contains a label (QtWidgets.QLabel) and a text field
         (QtWidgets.QLineEdit).

        Parameters
        ----------
        label (string) : the field label
        number (float) : the number that will be set to the field
        """
        assert (isinstance(number, int) or isinstance(number, float))
        number = float(number)

        super(FloatTField, self).__init__(label, "{:.1f}".format(number))
        self._format = "{:.2f}"
        self._value = number

    def __call__(self, x=None):
        if x is None:
            x = self.line_edit.text()
            x = float(x)
            return x
        else:
            x = float(x)
            self.line_edit.setText(self._format.format(x))
            self._value = x

    def set_format(self, s):
        self._format = s

def HLine():
    toto = QtWidgets.QFrame()
    toto.setFrameShape(QtWidgets.QFrame.HLine)
    toto.setFrameShadow(QtWidgets.QFrame.Sunken)
    return toto
