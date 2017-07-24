# -*- coding -*-
from __future__ import print_function, division

from PyQt5 import QtCore, QtWidgets
from numpy import sqrt

from .custom_widgets import ComboBox, FloatTField, IntTField, TextTField, HLine
from .methods import calc_finesse, calc_queensgate_constant


class PageScan(QtWidgets.QWidget):

    def __init__(self):
        super(PageScan, self).__init__()

        self.id = TextTField("Scan ID", '')
        self.id.add_button("Get")

        self.n_channels = IntTField("Number of channels:", 5)
        self.n_sweeps = IntTField("Number of sweeps:", 5)
        self.z_start = IntTField("Z Start [bcv]:", 1024)
        self.z_step = FloatTField("Z Step [bcv]:", -10)

        max_width = 75
        self.n_channels.set_field_max_width(max_width)
        self.n_sweeps.set_field_max_width(max_width)
        self.z_start.set_field_max_width(max_width)
        self.z_step.set_field_max_width(max_width)

        # Connect the buttons that will generate scan IDs
        self.id.button.clicked.connect(self.set_id)

        self.initUI()

    def initUI(self):

        # Scanning parameters -----------------------------
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)
        grid.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        grid.addWidget(self.z_start.label, 0, 0)
        grid.addWidget(self.z_start.line_edit, 0, 2)

        grid.addWidget(self.z_step.label, 1, 0)
        grid.addWidget(self.z_step.line_edit, 1, 2)

        grid.addWidget(self.n_channels.label, 2, 0)
        grid.addWidget(self.n_channels.line_edit, 2, 2)

        grid.addWidget(self.n_sweeps.label, 3, 0)
        grid.addWidget(self.n_sweeps.line_edit, 3, 2)

        grid.addWidget(self.id.label, 4, 0)
        grid.addWidget(self.id.line_edit, 4, 2)
        grid.addWidget(self.id.button, 4, 1)

        # Put inside a box layout to make it stick to the right ---
        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(grid)
        hbox.addStretch(1)

        self.setLayout(hbox)

    @property
    def number_of_channels(self):
        return self.n_channels()

    @property
    def number_of_sweeps(self):
        return self.n_sweeps()

    @property
    def total_steps(self):
        return self.number_of_channels * self.number_of_sweeps

    def set_id(self):

        from datetime import datetime
        now = datetime.utcnow()
        _id = now.strftime("SCAN_%Y%m%d_UTC%H%M%S")

        self.id(_id)


class PageCalibrationScan(PageScan):

    def __init__(self):

        self.ref_wavelength = FloatTField("Reference wavelength [A]:", 6600.0)
        self.fsr = FloatTField("Free Spectral Range [bcv]:", 0)
        self.fwhm = FloatTField("Full-width at half-maximum [bcv]:", 0.0)

        self.finesse = FloatTField("Finesse:", 0)
        self.finesse.add_button("Get")

        self.queensgate_constant = FloatTField("Queensgate constant:", 0)
        self.queensgate_constant.add_button("Get")

        self.sample_factor = FloatTField("Sample factor:", 2)
        self.overscan_factor = FloatTField("Overscan factor:", 1)

        self.set_scanpars_button = QtWidgets.QPushButton("Set scan parameters")

        self.finesse.connect(self.get_finesse)
        self.queensgate_constant.connect(self.get_queensgate_constant)

        super(PageCalibrationScan, self).__init__()

    def initUI(self):

        grid2 = QtWidgets.QGridLayout()
        grid2.addWidget(self.ref_wavelength.label, 0, 0)
        grid2.addWidget(self.ref_wavelength.line_edit, 0, 2)
        grid2.addWidget(self.fsr.label, 1, 0)
        grid2.addWidget(self.fsr.line_edit, 1, 2)
        grid2.addWidget(self.fwhm.label, 2, 0)
        grid2.addWidget(self.fwhm.line_edit, 2, 2)
        grid2.addWidget(HLine(), 3, 0, 1, 3)
        grid2.addWidget(self.finesse.label, 4, 0)
        grid2.addWidget(self.finesse.line_edit, 4, 2)
        grid2.addWidget(self.finesse.button, 4, 1)
        grid2.addWidget(self.queensgate_constant.label, 5, 0)
        grid2.addWidget(self.queensgate_constant.line_edit, 5, 2)
        grid2.addWidget(self.queensgate_constant.button, 5, 1)
        grid2.addWidget(HLine(), 6, 0, 1, 3)
        grid2.addWidget(self.sample_factor.label, 7, 0)
        grid2.addWidget(self.sample_factor.line_edit, 7, 2)
        grid2.addWidget(self.overscan_factor.label, 8, 0)
        grid2.addWidget(self.overscan_factor.line_edit, 8, 2)
        grid2.addWidget(HLine(), 9, 0, 1, 3)
        grid2.addWidget(self.set_scanpars_button, 10, 0, 1, 3)
        grid2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid2.setSpacing(2)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(grid2)
        vbox.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        vbox.setSpacing(5)
        self.setLayout(vbox)

    def get_finesse(self):
        f = calc_finesse(self.fsr(), self.fwhm())
        self.finesse(f)

    def get_queensgate_constant(self):
        f = calc_queensgate_constant(self.ref_wavelength(), self.fsr())
        self.queensgate_constant(f)

class PageScienceScan(PageCalibrationScan):

    def __init__(self):

        self.rest_wavelength = FloatTField("Rest wavelength [A]:", 6562.98)

        self.combo_box = ComboBox("",
            ["Observed wavelength [A]",
             "Systemic velocity [km / s]",
             "Redshift"]
        )

        self.calc = QtWidgets.QPushButton("Get")

        self.input = FloatTField("", 6562.98)
        self.output_1 = FloatTField("Redshift", 0)
        self.output_2 = FloatTField("Systemic velocity [km / s]", 0)
        self.cal_outputs_button = QtWidgets.QPushButton("Update outputs")
        self.on_combobox_change()

        #self.output_1.line_edit.setDisabled(True)
        #self.output_2.line_edit.setDisabled(True)

        self.output_1.set_format("{:0.5f}")
        self.output_2.set_format("{:0.5f}")

        self.sci_fsr = FloatTField("FSR for the observation [bcv]:", 0)
        self.sci_fsr.add_button("Get")

        # Connect ---
        self.combo_box.combo_box.currentIndexChanged.connect(
            self.on_combobox_change
        )
        self.combo_box.combo_box.currentIndexChanged.connect(
            self.input.line_edit.setFocus
        )

        self.cal_outputs_button.clicked.connect(
            self.on_combobox_change
        )

        self.input.line_edit.returnPressed.connect(
            self.on_combobox_change
        )

        self.sci_fsr.connect(
            self.calc_sci_fsr
        )

        super(PageScienceScan, self).__init__()

    def initUI(self):

        grid1 = QtWidgets.QGridLayout()
        grid1.setSpacing(2)
        grid1.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid1.addWidget(self.rest_wavelength.label, 0, 0)
        grid1.addWidget(self.rest_wavelength.line_edit, 0, 1)
        grid1.addWidget(self.combo_box.combo_box, 1, 0)
        grid1.addWidget(self.input.line_edit, 1, 1)
        grid1.addWidget(self.cal_outputs_button, 2, 0, 1, 2)
        grid1.addWidget(self.output_1.label, 3, 0)
        grid1.addWidget(self.output_1.line_edit, 3, 1)
        grid1.addWidget(self.output_2.label, 4, 0)
        grid1.addWidget(self.output_2.line_edit, 4, 1)
        grid1.addWidget(HLine(), 6, 0, 1, 2)

        grid2 = QtWidgets.QGridLayout()
        grid2.addWidget(self.ref_wavelength.label, 0, 0)
        grid2.addWidget(self.ref_wavelength.line_edit, 0, 2)
        grid2.addWidget(self.fsr.label, 1, 0)
        grid2.addWidget(self.fsr.line_edit, 1, 2)
        grid2.addWidget(self.fwhm.label, 2, 0)
        grid2.addWidget(self.fwhm.line_edit, 2, 2)
        grid2.addWidget(HLine(), 3, 0, 1, 3)
        grid2.addWidget(self.finesse.label, 4, 0)
        grid2.addWidget(self.finesse.line_edit, 4, 2)
        grid2.addWidget(self.finesse.button, 4, 1)
        grid2.addWidget(self.queensgate_constant.label, 5, 0)
        grid2.addWidget(self.queensgate_constant.line_edit, 5, 2)
        grid2.addWidget(self.queensgate_constant.button, 5, 1)
        grid2.addWidget(HLine(), 6, 0, 1, 3)
        grid2.addWidget(self.sci_fsr.label, 7, 0)
        grid2.addWidget(self.sci_fsr.line_edit, 7, 2)
        grid2.addWidget(self.sci_fsr.button, 7, 1)
        grid2.addWidget(HLine(), 8, 0, 1, 3)
        grid2.addWidget(self.sample_factor.label, 9, 0)
        grid2.addWidget(self.sample_factor.line_edit, 9, 2)
        grid2.addWidget(self.overscan_factor.label, 10, 0)
        grid2.addWidget(self.overscan_factor.line_edit, 10, 2)
        grid2.addWidget(HLine(), 11, 0, 1, 3)
        grid2.addWidget(self.set_scanpars_button, 12, 0, 1, 3)
        grid2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid2.setSpacing(2)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(grid1)
        vbox.addLayout(grid2)
        vbox.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        vbox.setSpacing(5)
        self.setLayout(vbox)

    def calc_sci_fsr(self):
        QGC = self.queensgate_constant()
        try:
            fsr = self.observed_wavelength / QGC
        except ZeroDivisionError as e:
            self.setStatusTip("Zero Division Error: Please check that the "
                              "Queensgate Constant value is not 0.")
            fsr = 0
        self.sci_fsr(fsr)

    def on_combobox_change(self):

        # Wavelength emitted
        w_emit = self.rest_wavelength()

        # Light Speed [km / s]
        c = 299792.458

        if self.combo_box() == "Redshift":
            z = self.input()

            w_obs = w_emit * (1 + z)
            self.output_1.set_label("Observed wavelength [A]:")
            self.output_1(w_obs)

            v = c * ((1 + z) ** 2 - 1) / ((1 + z) ** 2 + 1)
            self.output_2.set_label("Systemic velocity [km / s]:")
            self.output_2(v)

        elif self.combo_box() == "Observed wavelength [A]":
            w_obs = self.input()

            try:
                z = (w_obs - w_emit) / w_emit
            except ZeroDivisionError:
                z = 9999
                self.setStatusTip(
                    "Zero Division Error - "
                    "Please, check the value of the emission line.")

            self.output_1.set_label("Redshift:")
            self.output_1(z)

            v = c * ((1 + z) ** 2 - 1) / ((1 + z) ** 2 + 1)
            self.output_2.set_label("Systemic velocity [km / s]:")
            self.output_2(v)

        else:
            v = self.input()

            z = sqrt((1 + v / c) / (1 - v / c)) - 1
            self.output_1.set_label("Redshift:")
            self.output_1(z)

            w_obs = w_emit * (1 + z)
            self.output_2.set_label("Observed wavelength [A]:")
            self.output_2(w_obs)

        self.systemic_velocity = v
        self.redshift = z
        self.observed_wavelength = w_obs

        return