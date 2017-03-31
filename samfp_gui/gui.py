# -*- coding: utf-8 -*-

from __future__ import print_function, division

import configparser
import datetime
import logging
import os
import pkg_resources
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from . import scan

logging.basicConfig()
log = logging.getLogger("samfp.scan")
log.setLevel(logging.DEBUG)

home_folder = os.path.expanduser("~")

wavelength = {
        'Ha': 6562.78,
        'SIIf': 6716.47,
        'SIIF': 6730.85,
        'NIIf': 6548.03,
        'NIIF': 6583.41,
        'Ne 6600': 6598.9529
    }


class Main(QtWidgets.QMainWindow):

    config = {'temp_file': os.path.join(home_folder, '.samfp_temp.ini')}

    def __init__(self):
        super(Main, self).__init__()
        self.initUI()

    def initUI(self):

        # Set the font of the ToolTip windows
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        # Create the status bar
        self.status_bar = self.statusBar()

        # Create an action to leave the program
        load_action = self.get_load_action()
        save_action = self.get_save_action()
        exit_action = self.get_exit_action()

        # Create the menu bar
        menubar = self.menuBar()
        menu = menubar.addMenu('&File')
        menu.addAction(load_action)
        menu.addAction(save_action)
        menu.addAction(exit_action)

        # Create the toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(save_action)
        self.toolbar.addAction(load_action)
        self.toolbar.addAction(exit_action)

        # Create the central widget
        central = MyCentralWidget()
        self.setCentralWidget(central)

        # Set the geometry
        self.center()
        self.setWindowTitle('SAM-FP - Data-Acquisition')
        self.setWindowIcon(QtGui.QIcon('web.png'))

        self.load_temp_file()
        self.centralWidget().set_fp_pars()

        self.show()

    def center(self):

        # Figure out the screen resolution of our monitor.
        # And from this resolution, we get the center point.
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        # get a rectangle specifying the geometry of the main window.
        # This includes any window frame
        qr = self.frameGeometry()

        # Our rectangle has already its width and height.
        # Now we set the center of the rectangle to the center of the screen.
        # The rectangle's size is unchanged.
        qr.moveCenter(cp)

        # We move the top-left point of the application window to the top-left
        # point of the qr rectangle, thus centering the window on our screen.
        self.move(qr.topLeft())

    def closeEvent(self, event):

        self.save_temp_file()
        # reply = QtWidgets.QMessageBox.question(self, 'Message',
        #                                    "Are you sure to quit?",
        #                                    QtWidgets.QMessageBox.Yes |
        #                                    QtWidgets.QMessageBox.No,
        #                                    QtWidgets.QMessageBox.No)
        #
        # if reply == QtWidgets.QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

    def config_parse(self, config_file):

        central_widget = self.centralWidget()

        log.debug('Loading config file: {}'.format(config_file))

        cfg = configparser.RawConfigParser()
        cfg.read("{}".format(config_file))

        try:
            central_widget.basename(cfg.get('image', 'basename'))
            central_widget.comment(cfg.get('image', 'comment'))
            central_widget.path(cfg.get('image', 'dir'))
            central_widget.target_name(cfg.get('image', 'title'))
            central_widget.obs_type(cfg.get('image', 'type'))

            central_widget.exp_time(cfg.getfloat('obs', 'exptime'))
            central_widget.n_frames(cfg.getint('obs', 'nframes'))

            central_widget.scan_id(cfg.get('scan', 'id'))
            central_widget.n_channels(cfg.getint('scan', 'nchannels'))
            central_widget.n_sweeps(cfg.getint('scan', 'nsweeps'))
            central_widget.z_start(cfg.getint('scan', 'zstart'))
            central_widget.z_step(cfg.getfloat('scan', 'zstep'))
            central_widget.sleep_time(cfg.getfloat('scan', 'stime'))

            central_widget.notebook.setCurrentIndex(
                cfg.getint('gui', 'active_page')
            )

            # The calibration page ---
            central_widget.calib_page.lamp(cfg.get('calib', 'lamp'))
            central_widget.calib_page.wavelength(
                wavelength[central_widget.calib_page.lamp()])

            if cfg.getboolean('fp', 'low_res_fabry_perot'):
                central_widget.fp_low_res_rb.setChecked(True)
            else:
                central_widget.fp_high_res_rb.setChecked(True)

            central_widget.fp_gap_size(
                cfg.getfloat('fp', 'gap_size')
            )
            central_widget.fp_order(
                cfg.getfloat('fp', 'order')
            )
            central_widget.queensgate_constant(
                cfg.getfloat('fp', 'queensgate_constant')
            )
            central_widget.finesse(
                cfg.getfloat('fp', 'finesse')
            )
            central_widget.free_spectral_range(
                cfg.getfloat('fp', 'free_spectral_range')
            )
            central_widget.fwhm(
                cfg.getfloat('fp', 'fwhm')
            )
            central_widget.sampling(
                cfg.getfloat('fp', 'sample_factor')
            )
            central_widget.overscan_factor(
                cfg.getfloat('fp', 'overscan_factor')
            )

        except configparser.NoOptionError as error:
            log.warning("{}".format(error.option) + \
                        " option not found in the input config file")

        except configparser.NoSectionError as error:
            log.warning("{}".format(error.section) + \
                        " section not found in the input config file")

    def config_generate(self):

        central_widget = self.centralWidget()

        cfg = configparser.RawConfigParser()
        cfg.add_section('image')
        cfg.set('image', 'basename', central_widget.basename())
        cfg.set('image', 'comment', central_widget.comment())
        cfg.set('image', 'dir', central_widget.path())
        cfg.set('image', 'title', central_widget.target_name())
        cfg.set('image', 'type',
                central_widget.obs_type.combo_box.currentText())

        cfg.add_section('obs')
        cfg.set('obs', 'exptime', central_widget.exp_time())
        cfg.set('obs', 'nframes', central_widget.n_frames())

        cfg.add_section('scan')
        cfg.set('scan', 'id', central_widget.scan_id())
        cfg.set('scan', 'nchannels', central_widget.n_channels())
        cfg.set('scan', 'nsweeps', central_widget.n_sweeps())
        cfg.set('scan', 'stime', central_widget.sleep_time())
        cfg.set('scan', 'zstart', central_widget.z_start())
        cfg.set('scan', 'zstep', central_widget.z_step())

        cfg.add_section('gui')
        cfg.set('gui', 'active_page', central_widget.notebook.currentIndex())

        cfg.add_section('calib')
        cfg.set('calib', 'lamp', central_widget.calib_page.lamp())
        cfg.set('calib', 'wavelength', central_widget.calib_page.wavelength())
        
        cfg.add_section('science')


        cfg.add_section('fp')
        if central_widget.fp_low_res_rb.isChecked():
            cfg.set('fp', 'low_res_fabry_perot', True)
        else:
            cfg.set('fp', 'low_res_fabry_perot', False)

        cfg.set('fp', 'order',
                central_widget.fp_order())
        cfg.set('fp', 'gap_size',
                central_widget.fp_gap_size())
        cfg.set('fp', 'queensgate_constant',
                central_widget.queensgate_constant())
        cfg.set('fp', 'finesse',
                central_widget.finesse())
        cfg.set('fp', 'free_spectral_range',
                central_widget.free_spectral_range())
        cfg.set('fp', 'fwhm',
                central_widget.fwhm())
        cfg.set('fp', 'sample_factor',
                central_widget.sampling())
        cfg.set('fp', 'overscan_factor',
                central_widget.overscan_factor())

        return cfg

    def get_exit_action(self):

        icon_path = pkg_resources.resource_filename(
            'samfp_gui', 'icons/close.png')

        exit_action = QtWidgets.QAction(QtGui.QIcon(icon_path),'&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        return exit_action

    def get_load_action(self):

        icon_path = pkg_resources.resource_filename(
            'samfp_gui', 'icons/load-icon.png')

        load_action = QtWidgets.QAction(QtGui.QIcon(icon_path), '&Open', self)
        load_action.setShortcut('Ctrl+O')
        load_action.setStatusTip('Load config file.')
        load_action.triggered.connect(self.load_config_file)

        return load_action

    def get_save_action(self):

        icon_path = pkg_resources.resource_filename(
            'samfp_gui', 'icons/save-icon.png')

        save_action = QtWidgets.QAction(QtGui.QIcon(icon_path), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save config file.')
        save_action.triggered.connect(self.save_config_file)

        return save_action

    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def load_config_file(self):
        # TODO Isolate only configuration files
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '.')
        fname = str(fname)
        self.config_parse(fname)

    def load_temp_file(self):
        if os.path.exists(self.config['temp_file']):
            self.config_parse(self.config['temp_file'])
        else:
            log.debug('Temp config file does not exists.')

    def save_config_file(self):
        """Save a new configuration file"""
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save', os.getcwd())
        fname = str(fname)

        temp_config = self.config_generate()
        with open(fname, 'w') as foo:
            temp_config.write(foo)

    def save_temp_file(self):
        """Save a temporary file for persistance"""

        temp_config = self.config_generate()
        with open(self.config['temp_file'], 'w') as foo:
            temp_config.write(foo)

        log.debug("Saved config file %s" % self.config['temp_file'])

class MyCentralWidget(QtWidgets.QFrame):

    def __init__(self):
        super(MyCentralWidget, self).__init__()
        self.initUI()

    def initUI(self):

        self.bottom_group = self.init_bottom_panel()
        self.left_group = self.init_left_panel()
        self.middle_group = self.init_middle_panel()
        self.right_group = self.init_right_panel()
        self.top_group = self.init_top_panel()

        self.do_connections()

        # Put all of them in the main grid -------------------------------------
        main_grid = QtWidgets.QGridLayout()

        main_grid.addWidget(self.top_group, 0, 0, 1, 3)
        main_grid.addWidget(self.left_group, 1, 0)
        main_grid.addWidget(self.middle_group, 1, 1)
        main_grid.addWidget(self.right_group, 1, 2)
        main_grid.addWidget(self.bottom_group, 3, 0, 1, 3)

        main_grid.setAlignment(QtCore.Qt.AlignTop)
        main_grid.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(main_grid)

        w = self.get_wavelength()

        # Add the thread for the scan ------------------------------------------
        self.timer = QtCore.QBasicTimer()
        self.step = 0

    def do_connections(self):

        self.scan_button.clicked.connect(self.scan_start)
        self.abort_button.clicked.connect(self.scan_abort)
        self.set_scan_button.clicked.connect(self.set_scan_pars)

        self.scan_id.line_edit.returnPressed.connect(self.get_id)

        # Connect handlers -----------------------------------------------------
        self.fp_low_res_rb.setChecked(True)

        self.fp_low_res_rb.clicked.connect(self.set_fp_pars)
        self.fp_high_res_rb.clicked.connect(self.set_fp_pars)

        self.calib_page.lamp.combo_box.currentIndexChanged.connect(
            self.on_lamp_change)

        self.queensgate_constant.button.clicked.connect(
            self.get_queensgate_constant)
        self.queensgate_constant.line_edit.returnPressed.connect(
            self.get_queensgate_constant)

        self.finesse.button.clicked.connect(self.get_finesse)
        self.finesse.line_edit.returnPressed.connect(self.get_finesse)


    def get_finesse(self):
        """
        Use the current FSR and FWHM to calculate and set the Finesse.
        """
        try:
            self.finesse(calc_finesse(self.free_spectral_range(), self.fwhm()))

        except ZeroDivisionError as error:
            main_widget = self.window()
            main_widget.status_bar.showMessage(
                "Error: Zero division while calculating the Finesse."
            )

    def get_queensgate_constant(self):
        """
        Use the current wavelength and the free-spectral-range to calculate
        and set the Queensgate Constant.
        """

        w = self.get_wavelength()
        FSR = self.free_spectral_range()

        try:
            QGC = calc_queensgate_constant(w, FSR)
            self.queensgate_constant(QGC)

        except ZeroDivisionError as error:

            main_widget = self.window()
            main_widget.status_bar.showMessage(
                "Error: Zero division while calculating the Queensgate "
                "Constant."
            )

    def get_id(self):
        now = datetime.datetime.now()
        s = now.strftime("SCAN_%Y%m%d_UTC%H%M%S")
        self.scan_id(s)

    def get_wavelength(self):

        if self.calib_page.isActiveWindow():
            key = str(self.calib_page.lamp.combo_box.currentText())
            w = wavelength[key]
        else:
            w = self.sci_page.wavelength()

        return w

    def init_bottom_panel(self):

        self.scan_button = QtWidgets.QPushButton("Scan")
        self.abort_button = QtWidgets.QPushButton("Abort")
        self.progress_bar = QtWidgets.QProgressBar()

        self.scan_button.setEnabled(True)
        self.abort_button.setDisabled(True)
        self.progress_bar.setDisabled(True)

        bottom_group = QtWidgets.QGroupBox()

        bottom_grid = QtWidgets.QGridLayout()
        bottom_grid.setSpacing(5)

        bottom_grid.addWidget(self.scan_button, 10, 0)
        bottom_grid.addWidget(self.abort_button, 10, 1)
        bottom_grid.addWidget(self.progress_bar, 10, 2)

        bottom_grid.setAlignment(QtCore.Qt.AlignLeft)
        bottom_grid.setAlignment(QtCore.Qt.AlignTop)
        bottom_group.setLayout(bottom_grid)

        return bottom_group

    def init_left_panel(self):

        self.obs_type = MyComboBox(
            "Observation type: ", ["DARK", "DFLAT", "OBJECT", "SFLAT", "ZERO"])

        self.target_name = MyLineEdit("Target name:", "")
        self.comment = MyLineEdit("Comment:", "")

        self.exp_time = MyLineEdit_Float("Exposure time [s]:", -1)
        self.n_frames = MyLineEdit_Int("Frames per channel:", -1)

        self.scan_id = MyLineEdit("Scan ID:", "")
        self.n_channels = MyLineEdit_Int("Number of channels:", 1)
        self.n_sweeps = MyLineEdit_Int("Number of sweeps:", 1)
        self.z_start = MyLineEdit_Int("Z Start [bcv]:", 1024)
        self.z_step = MyLineEdit_Float("Z Step [bcv]:", 0)
        self.sleep_time = MyLineEdit_Float("Sleep time [s]:", 0)

        self.scan_id.add_button("Get ID")
        self.scan_id.button.clicked.connect(self.get_id)
        self.scan_id.line_edit.setMinimumWidth(200)

        group = QtWidgets.QGroupBox()

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.obs_type.label, 0, 0)
        grid.addWidget(self.obs_type.combo_box, 0, 1, 1, 2)

        grid.addWidget(self.target_name.label, 1, 0)
        grid.addWidget(self.target_name.line_edit, 1, 1, 1, 2)

        grid.addWidget(self.comment.label, 2, 0)
        grid.addWidget(self.comment.line_edit, 2, 1, 1, 2)

        grid.addWidget(self.HLine(), 3, 0, 1, 3)

        grid.addWidget(self.exp_time.label, 4, 0)
        grid.addWidget(self.exp_time.line_edit, 4, 1, 1, 2)

        grid.addWidget(self.n_frames.label, 5, 0)
        grid.addWidget(self.n_frames.line_edit, 5, 1, 1, 2)

        grid.addWidget(self.HLine(), 6, 0, 1, 3)

        grid.addWidget(self.scan_id.label, 7, 0)
        grid.addWidget(self.scan_id.line_edit, 8, 0, 1, 2)
        grid.addWidget(self.scan_id.button, 8, 2)

        grid.addWidget(self.n_sweeps.label, 9, 0)
        grid.addWidget(self.n_sweeps.line_edit, 9, 1, 1, 2)

        grid.addWidget(self.n_channels.label, 10, 0)
        grid.addWidget(self.n_channels.line_edit, 10, 1)

        grid.addWidget(self.z_start.label, 11, 0)
        grid.addWidget(self.z_start.line_edit, 11, 1)

        grid.addWidget(self.z_step.label, 12, 0)
        grid.addWidget(self.z_step.line_edit, 12, 1)

        grid.addWidget(self.sleep_time.label, 13, 0)
        grid.addWidget(self.sleep_time.line_edit, 13, 1)

        grid.setAlignment(QtCore.Qt.AlignLeft)
        grid.setAlignment(QtCore.Qt.AlignTop)
        group.setLayout(grid)

        return group

    def init_top_panel(self):

        self.basename = MyLineEdit("Basename", "")
        self.path = MyLineEdit("Path:", "")

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.basename.label, 0, 0)
        grid.addWidget(self.basename.line_edit, 1, 0)
        grid.addWidget(self.path.label, 2, 0)
        grid.addWidget(self.path.line_edit, 3, 0)

        grid.setAlignment(QtCore.Qt.AlignLeft)
        grid.setAlignment(QtCore.Qt.AlignTop)

        group = QtWidgets.QGroupBox()
        group.setLayout(grid)

        return group

    def init_middle_panel(self):

        # Initialize widgets ---
        self.fp_label = QtWidgets.QLabel("Fabry-Perot")
        self.fp_low_res_rb = QtWidgets.QRadioButton("Low-Resolution")
        self.fp_high_res_rb = QtWidgets.QRadioButton("High-Resolution")

        self.fp_order = MyLineEdit_Float("Interference order at Ha:", 0)
        self.fp_gap_size = MyLineEdit_Float("Gap size [um]:", 0)

        self.queensgate_constant = MyLineEdit_Float(
            "Queensgate Constant [A / bcv]:", 0)
        self.finesse = MyLineEdit_Float(
            "Finesse [--]:", 0)
        self.free_spectral_range = MyLineEdit_Float(
            "Free Spectral Range [bcv]:", 0)
        self.fwhm = MyLineEdit_Float(
            "Full-width at half-maximum [bcv]:", 0)

        self.sampling = MyLineEdit_Float(
            "Sampling [bcv / step]:", 1)

        self.overscan_factor = MyLineEdit_Float(
            "Overscan factor:", 1)

        self.queensgate_constant.add_button("Get")
        self.finesse.add_button("Get")

        self.set_scan_button = QtWidgets.QPushButton("Set scan parameters")

        # Add them to the grid ---
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.fp_label, 0, 0, 1, 3)
        grid.addWidget(self.fp_low_res_rb, 1, 0, 1, 3)
        grid.addWidget(self.fp_high_res_rb, 2, 0, 1, 3)

        grid.addWidget(self.HLine(), 3, 0, 1, 3)

        grid.addWidget(self.fp_gap_size.label, 4, 0)
        grid.addWidget(self.fp_gap_size.line_edit, 4, 1, 1, 2)

        grid.addWidget(self.free_spectral_range.label, 5, 0)
        grid.addWidget(self.free_spectral_range.line_edit, 5, 1, 1, 2)

        grid.addWidget(self.fwhm.label, 6, 0)
        grid.addWidget(self.fwhm.line_edit, 6, 1, 1, 2)

        grid.addWidget(self.queensgate_constant.label, 7, 0)
        grid.addWidget(self.queensgate_constant.line_edit, 8, 0, 1, 2)
        grid.addWidget(self.queensgate_constant.button, 8, 2)

        grid.addWidget(self.finesse.label, 9, 0)
        grid.addWidget(self.finesse.line_edit, 10, 0, 1, 2)
        grid.addWidget(self.finesse.button, 10, 2)

        grid.addWidget(self.HLine(), 11, 0, 1, 3)

        grid.addWidget(self.sampling.label, 12, 0)
        grid.addWidget(self.sampling.line_edit, 12, 1, 1, 2)

        grid.addWidget(self.overscan_factor.label, 13, 0)
        grid.addWidget(self.overscan_factor.line_edit, 13, 1, 1, 2)

        grid.addWidget(self.set_scan_button, 14, 0, 1, 3)

        grid.setAlignment(QtCore.Qt.AlignLeft)
        grid.setAlignment(QtCore.Qt.AlignTop)

        group = QtWidgets.QGroupBox()
        group.setLayout(grid)
        
        return group

    def init_right_panel(self):

        self.calib_page = PageCalibrationScan()
        self.sci_page = PageScienceScan()

        self.notebook = QtWidgets.QTabWidget()
        self.notebook.addTab(self.calib_page, "Calibration Scan")
        self.notebook.addTab(self.sci_page, "Science Scan")

        return self.notebook

    def scan_abort(self):

        self.timer.stop()
        self.scan_button.setEnabled(True)
        self.abort_button.setDisabled(True)
        self.progress_bar.setDisabled(True)
        self.step = 0

    def on_lamp_change(self):
        """
        Does nothing for now. Check with Philippe if he wants this to deppend on
        the source wavelength or not.
        """
        if self.calib_page.lamp() in wavelength.keys():
            w = wavelength[self.calib_page.lamp()]
            self.calib_page.wavelength(w)
        # TODO - Change other parameters that deppend on wavelength
        # TODO - Change paramaters when CALIB / SCI is selected
            # and when the custom mode too

    def scan_start(self):

        self.current_sweep = 1
        self.current_channel = 1
        self.z = self.z_start()

        self.total_sweeps = self.n_sweeps()
        self.total_channels = self.n_channels()
        self.total_steps = self.total_channels * self.total_sweeps
        self.step_fraction = 1. / self.total_steps * 100

        self.timer.start(50, self)
        self.scan_button.setDisabled(True)
        self.abort_button.setEnabled(True)
        self.progress_bar.setEnabled(True)

        scan.set_image_path(self.path())
        scan.set_image_basename(self.basename())

        scan.set_image_type(self.obs_type())
        scan.set_target_name(self.target_name())
        scan.set_comment(self.comment())
        scan.set_image_nframes(self.n_frames())
        scan.set_image_exposure_time(self.exp_time())

        scan.set_scan_id(self.scan_id())
        scan.set_scan_start(self.z_start())
        scan.set_scan_nchannels(self.n_channels())

        self.z = self.z_start()
        self.current_sweep = 1
        self.current_channel = 1

    def set_fp_pars(self):

        if self.fp_low_res_rb.isChecked():
            gap_size = 44.
        else:
            gap_size = 200.

        if self.calib_page.isActiveWindow():
            w = wavelength[self.calib_page.lamp()]
        else:
            w = self.sci_page.wavelength()

        self.fp_gap_size(gap_size)
        self.fp_order(calc_order(w, gap_size))

    def set_scan_pars(self):

        overscan_factor = self.overscan_factor()
        sampling = self.sampling()

        n_channels = 2 * self.finesse()
        z_step = self.fwhm() / sampling

        n_channels = round(overscan_factor * n_channels)

        self.n_channels(n_channels)
        self.z_step(- z_step)


    def timerEvent(self, e):

        if self.step >= 100:
            self.timer.stop()
            self.scan_abort()
            return

        if self.z < 0 or self.z > 4095:
            self.timer.stop()
            self.scan_abort()

        log.debug("Sweep: {}, Channel {}, Z {}".format(
            self.current_sweep, self.current_channel, self.z))

        scan.set_scan_current_z(int(round(self.z)))
        scan.set_scan_current_sweep(self.current_sweep)

        time.sleep(self.sleep_time())
        scan.expose()

        self.step += self.step_fraction
        self.progress_bar.setValue(self.step)

        self.current_channel += 1
        self.z += self.z_step()

        if self.current_channel > self.total_channels:
            self.current_channel = 1
            self.current_sweep += 1
            self.z = self.z_start()

    def HLine(self):
        toto = QtWidgets.QFrame()
        toto.setFrameShape(QtWidgets.QFrame.HLine)
        toto.setFrameShadow(QtWidgets.QFrame.Sunken)
        return toto


class MyComboBox(QtWidgets.QWidget):

    def __init__(self, label, options):

        super(MyComboBox, self).__init__()

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


class MyLineEdit(QtWidgets.QWidget):

    def __init__(self, label, value):
        """
        Initialize field that contains a label (QtWidgets.QLabel) and a text field
         (QtWidgets.QLineEdit).

        Parameters
        ----------
        label (string) : the field label
        text (string) : the text that will be inside the text box
        """
        super(MyLineEdit, self).__init__()

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


class MyLineEdit_Int(MyLineEdit):

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

        super(MyLineEdit_Int, self).__init__(label, "{:d}".format(number))
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


class MyLineEdit_Float(MyLineEdit):

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

        super(MyLineEdit_Float, self).__init__(label, "{:.1f}".format(number))
        self._value = number

    def __call__(self, x=None):
        if x is None:
            x = self.line_edit.text()
            x = float(x)
            return x
        else:
            assert (isinstance(x, int) or isinstance(x, float))
            x = float(x)
            self.line_edit.setText("{:.1f}".format(x))
            self._value = x

class PageCalibrationScan(QtWidgets.QWidget):

    def __init__(self):
        super(PageCalibrationScan, self).__init__()
        self.initUI()

    def initUI(self):

        self.lamp = MyComboBox("Lamp: ", wavelength.keys())
        self.wavelength = MyLineEdit_Float("Wavelength [A]", 0)

        key = self.lamp()
        self.wavelength(wavelength[key])

        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.lamp.label, 0, 0)
        grid.addWidget(self.lamp.combo_box, 0, 1)

        grid.addWidget(self.wavelength.label, 1, 0)
        grid.addWidget(self.wavelength.line_edit, 1, 1)

        grid.setAlignment(QtCore.Qt.AlignLeft)
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)


class PageScienceScan(QtWidgets.QWidget):
    def __init__(self):
        super(PageScienceScan, self).__init__()

        # These are the variables that this page will have
        self.redshift = None
        self.heliocentric_velocity = None
        self.systemic_velocity = None
        self.rest_wavelength = None
        self.wavelength = None

        self.initUI()

    def initUI(self):

        # Initialize fields ---
        self.rest_wavelength = MyLineEdit_Float("Rest wavelength [A]:", -1)
        self.redshift = MyLineEdit_Float("Redshift [-]:", -1)
        self.systemic_velocity = MyLineEdit_Float("Systemic velocity [km / s]:", -1)
        self.wavelength = MyLineEdit_Float("Observed wavelength [A]:", -1)

        self.systemic_velocity.add_button("Get")
        self.wavelength.add_button("Get")

        # Put them inside the grid ---
        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.rest_wavelength.label, 0, 0)
        grid.addWidget(self.rest_wavelength.line_edit, 0, 1, 1, 2)

        grid.addWidget(self.redshift.label, 1, 0)
        grid.addWidget(self.redshift.line_edit, 1, 1, 1, 2)

        grid.addWidget(self.systemic_velocity.label, 2, 0)
        grid.addWidget(self.systemic_velocity.line_edit, 3, 0, 1, 2)
        grid.addWidget(self.systemic_velocity.button, 3, 2)

        grid.addWidget(self.wavelength.label, 4, 0)
        grid.addWidget(self.wavelength.line_edit, 5, 0, 1, 2)
        grid.addWidget(self.wavelength.button, 5, 2)

        grid.setAlignment(QtCore.Qt.AlignLeft)
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

        self.systemic_velocity.button.clicked.connect(self.get_systemic_velocity)

    def get_systemic_velocity(self):

        print(const.c.to('km/s'))



def calc_order(wavelength, gap_size):
    """
    Returns the FP interferential order.

    Parameters
    ----------
    wavelength (float):
    gap_size (float):

    Returns
    -------
    order (float)
    """
    return 2 * (gap_size * 1e-6) / (wavelength * 1e-10)



def calc_finesse(FSR, FWHM):
    """
    Returns the FP Finesse.

    Parameters
    ----------
    FSR (float) : free-spectral-range in BCV or A
    FWHM (float) : full-width-at-half-maximum in BCV or A

    Returns
    -------
    F (float) : the finesse

    Observations
    ------------
    Both FSR and FWHM have to have same units.
    """
    return float(FSR) / float(FWHM)


def calc_queensgate_constant(wavelength, free_spectra_range_bcv):
    """
    Returns the Fabry-Perot's Queensgate Constant.

    Parameters
    ----------
    wavelength (float):
    free_spectra_range_bcv (float):


    Returns
    -------
    queensgate_constant (float) :
    """
    return wavelength / free_spectra_range_bcv


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle("cleanlooks")
    ex = Main()
    sys.exit(app.exec_())