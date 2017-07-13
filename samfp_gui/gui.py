# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import logging
import os
import sys
import time

import configparser
import pkg_resources
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from . import scan
from .custom_widgets import ComboBox, FloatTField, IntTField, TextTField, HLine
from .pages import PageScan, PageCalibrationScan, PageScienceScan

logging.basicConfig()
log = logging.getLogger("samfp.scan")
log.setLevel(logging.DEBUG)

wavelength = {
    'Ha': 6562.78,
    'SIIf': 6716.47,
    'SIIF': 6730.85,
    'NIIf': 6548.03,
    'NIIF': 6583.41,
    'Ne 6600': 6598.9529
}


class MainWindow(QtWidgets.QMainWindow):
    temp_cfg_file = os.path.join(os.path.expanduser("~"), '.samfp_temp.cfg')

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):

        # Set the font of the ToolTip windows
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        # Run in simulation mode?
        self._am_i_simulating = True

        # Create the status bar
        self.status_bar = self.statusBar()

        # Create an action to leave the program
        self.load_action = self.get_load_action()
        self.save_action = self.get_save_action()
        self.toogle_connect_action = self.get_toogle_connect_action()
        self.exit_action = self.get_exit_action()

        # Create the menu bar
        self.menubar = self.menuBar()
        self.menubar._file = self.menubar.addMenu('&File')
        self.menubar._file.addAction(self.load_action)
        self.menubar._file.addAction(self.save_action)
        self.menubar._file.addAction(self.exit_action)

        # Create the toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.load_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.toogle_connect_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.exit_action)

        # Create the central widget
        central = MyCentralWidget()
        self.setCentralWidget(central)

        # Set the geometry
        self.center()
        self.setWindowTitle('SAM-FP - Data-Acquisition')
        self.setWindowIcon(QtGui.QIcon('web.png'))

        # Load the persistence configuration file
        self.load_config_file(self.temp_cfg_file)

        # Display the main window
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
        self.save_config_file(self.temp_cfg_file)
        return

    def config_parse(self, config_file):

        _cw = self.centralWidget()

        cfg = configparser.RawConfigParser()
        cfg.read("{:s}".format(config_file))

        _cw.basename(cfg.get('file', 'basename'))
        _cw.path(cfg.get('file', 'path'))

        _cw.binning(cfg.get('obs', 'binning'))
        _cw.comment(cfg.get('obs', 'comment'))
        _cw.exp_time(cfg.getfloat('obs', 'exptime'))
        _cw.n_frames(cfg.getint('obs', 'nframes'))
        _cw.obs_type(cfg.get('obs', 'type'))
        _cw.target_name(cfg.get('obs', 'title'))

        _cw.fp(cfg.get('fp', 'name'))
        _cw.fp_gap_size(cfg.get('fp', 'gap_size'))

        scan_page = _cw.page_scan
        scan_page.id(cfg.get('scan', 'id'))
        scan_page.n_channels(cfg.getint('scan', 'nchannels'))
        scan_page.n_sweeps(cfg.getint('scan', 'nsweeps'))
        scan_page.z_start(cfg.getint('scan', 'zstart'))
        scan_page.z_step(cfg.getint('scan', 'zstep'))

        calib_page = _cw.page_calibration
        calib_page.n_channels(cfg.getint('calib', 'nchannels'))
        calib_page.n_sweeps(cfg.getint('calib', 'nsweeps'))
        calib_page.z_start(cfg.getfloat('calib', 'zstart'))
        calib_page.z_step(cfg.getfloat('calib', 'zstep'))
        calib_page.ref_wavelength(cfg.getfloat('calib', 'ref_wav'))
        calib_page.fsr(cfg.getfloat('calib', 'fsr'))
        calib_page.fwhm(cfg.getfloat('calib', 'fwhm'))
        calib_page.finesse(cfg.getfloat('calib', 'finess'))
        calib_page.queensgate_constant(cfg.getfloat('calib', 'qgc'))
        calib_page.sample_factor(cfg.getfloat('calib', 'sample'))
        calib_page.overscan_factor(cfg.getfloat('calib', 'overscan'))

        sci_page = _cw.page_science
        sci_page.n_channels(cfg.getint('science', 'nchannels'))
        sci_page.n_sweeps(cfg.getint('science', 'nsweeps'))
        sci_page.z_start(cfg.getfloat('science', 'zstart'))
        sci_page.z_step(cfg.getfloat('science', 'zstep'))
        sci_page.ref_wavelength(cfg.getfloat('science', 'ref_wav'))
        sci_page.fsr(cfg.getfloat('science', 'fsr'))
        sci_page.fwhm(cfg.getfloat('science', 'fwhm'))
        sci_page.finesse(cfg.getfloat('science', 'finess'))
        sci_page.queensgate_constant(cfg.getfloat('science', 'qgc'))
        sci_page.sample_factor(cfg.getfloat('science', 'sample'))
        sci_page.overscan_factor(cfg.getfloat('science', 'overscan'))
        sci_page.rest_wavelength(cfg.getfloat('science', 'rest_wav'))
        sci_page.combo_box(cfg.get('science', 'combo_box'))
        sci_page.sci_fsr(cfg.getfloat('science', 'fsr_obs'))

        z = cfg.getfloat('science', 'redshift')
        w_obs = cfg.getfloat('science', 'obs_wav')
        v = cfg.getfloat('science', 'velocity')

        sci_page.systemic_velocity = v
        sci_page.redshift = z
        sci_page.observed_wavelength = w_obs

        if sci_page.combo_box() == "Redshift":
            sci_page.input(z)
            sci_page.output_1.set_label("Observed wavelength [A]")
            sci_page.output_1(w_obs)
            sci_page.output_2.set_label("Systemic velocity [km / s]")
            sci_page.output_2(v)

        elif sci_page.combo_box() == "Observed wavelength [A]":
            sci_page.input(w_obs)
            sci_page.output_1(z)
            sci_page.output_2(v)
        else:
            sci_page.input(v)
            sci_page.output_1(z)
            sci_page.output_2(w_obs)

        _cw.notebook.setCurrentIndex(cfg.getint('gui', 'active_page'))

    def config_generate(self):

        _cw = self.centralWidget()
        _main = self.parent()

        cfg = configparser.RawConfigParser()

        cfg.add_section('file')
        cfg.set('file', 'basename', _cw.basename())
        cfg.set('file', 'path', _cw.path())

        cfg.add_section('obs')
        cfg.set('obs', 'binning', _cw.binning())
        cfg.set('obs', 'comment', _cw.comment())
        cfg.set('obs', 'exptime', _cw.exp_time())
        cfg.set('obs', 'nframes', _cw.n_frames())
        cfg.set('obs', 'title', _cw.target_name())
        cfg.set('obs', 'type', _cw.obs_type())

        cfg.add_section('fp')
        cfg.set('fp', 'name', _cw.fp())
        cfg.set('fp', 'gap_size', _cw.fp_gap_size())

        cfg.add_section('gui')
        cfg.set('gui', 'simulation', _main._am_i_simulation)
        cfg.set('gui', 'active_page', _cw.notebook.currentIndex())

        scan_page = _cw.page_scan
        cfg.add_section('scan')
        cfg.set('scan', 'id', scan_page.id())
        cfg.set('scan', 'nchannels', scan_page.n_channels())
        cfg.set('scan', 'nsweeps', scan_page.n_sweeps())
        cfg.set('scan', 'zstart', scan_page.z_start())
        cfg.set('scan', 'zstep', scan_page.z_step())

        calib_page = _cw.page_calibration
        cfg.add_section('calib')
        cfg.set('calib', 'nchannels', calib_page.n_channels())
        cfg.set('calib', 'nsweeps', calib_page.n_sweeps())
        cfg.set('calib', 'zstart', calib_page.z_start())
        cfg.set('calib', 'zstep', calib_page.z_step())
        cfg.set('calib', 'ref_wav', calib_page.ref_wavelength())
        cfg.set('calib', 'fsr', calib_page.fsr())
        cfg.set('calib', 'fwhm', calib_page.fwhm())
        cfg.set('calib', 'finess', calib_page.finesse())
        cfg.set('calib', 'qgc', calib_page.queensgate_constant())
        cfg.set('calib', 'sample', calib_page.sample_factor())
        cfg.set('calib', 'overscan', calib_page.overscan_factor())

        sci_page = _cw.page_science
        cfg.add_section('science')
        cfg.set('science', 'nchannels', sci_page.n_channels())
        cfg.set('science', 'nsweeps', sci_page.n_sweeps())
        cfg.set('science', 'zstart', sci_page.z_start())
        cfg.set('science', 'zstep', sci_page.z_step())
        cfg.set('science', 'ref_wav', sci_page.ref_wavelength())
        cfg.set('science', 'fsr', sci_page.fsr())
        cfg.set('science', 'fwhm', sci_page.fwhm())
        cfg.set('science', 'finess', sci_page.finesse())
        cfg.set('science', 'qgc', sci_page.queensgate_constant())
        cfg.set('science', 'sample', sci_page.sample_factor())
        cfg.set('science', 'overscan', sci_page.overscan_factor())
        cfg.set('science', 'rest_wav', sci_page.rest_wavelength())
        cfg.set('science', 'combo_box', sci_page.combo_box())

        if sci_page.combo_box() == "Redshift":
            z = sci_page.input()
            w_obs = sci_page.output_1()
            v = sci_page.output_2()
        elif sci_page.combo_box() == "Observed wavelength [A]":
            w_obs = sci_page.input()
            z = sci_page.output_1()
            v = sci_page.output_2()
        else:
            v = sci_page.input()
            z = sci_page.output_1()
            w_obs = sci_page.output_2()

        cfg.set('science', 'redshift', z)
        cfg.set('science', 'velocity', v)
        cfg.set('science', 'obs_wav', w_obs)
        cfg.set('science', 'fsr_obs', sci_page.sci_fsr())

        return cfg

    def get_exit_action(self):

        icon_path = pkg_resources.resource_filename(
            'samfp_gui', 'icons/close-icon.png')

        exit_action = QtWidgets.QAction(QtGui.QIcon(icon_path), '&Exit', self)
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

    def get_toogle_connect_action(self):

        icon_path = pkg_resources.resource_filename(
            'samfp_gui', 'icons/disconnected-icon.png')

        toogle_connect_action = QtWidgets.QAction(QtGui.QIcon(icon_path),
                                                  '&Toogle Connect', self)
        toogle_connect_action.setStatusTip('Start/Stop simulation mode.')
        toogle_connect_action.triggered.connect(self.toogle_connection)

        return toogle_connect_action

    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def load_config_file(self, filename=False):

        if not filename:
            filename = self.load_file_dialog()

        try:
            self.config_parse(filename)
            log.debug("Loading configuration from: {:s}".format(filename))

        except configparser.NoOptionError as error:
            log.error("{}".format(error.option) +
                      " option not found in the input config file.")

        except configparser.NoSectionError as error:
            log.error("{}".format(error.section) +
                      " section not found in the input config file.")

        except configparser.MissingSectionHeaderError as error:
            log.error("{:s}".format(error.source) +
                      " is not a valid configuration file.")

    def load_file_dialog(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '.',
            # "Config Files (*.cfg);;Text Files (*.txt);;All Files (*)",
            options=options
        )

        return filename

    def save_config_file(self, filename=False):
        """
        Save a new configuration file.

        Parameters
        ----------
        filename (string) : The name of the file that will hold the
            configuration. If None is given, open a dialog to ask the
            user for one.
        """

        if not filename:
            filename = self.save_file_dialog()

        temp_config = self.config_generate()
        with open(filename, 'w') as foo:
            temp_config.write(foo)

        log.debug("Saved config file: {:s}".format(filename))
        self.setStatusTip("Saved config file: {:s}".format(filename))

    def save_file_dialog(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        filename, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "",
            "Configuration Files (*.cfg);; All Files (*);;Text Files (*.txt)",
            options=options
        )

        if os.path.splitext(filename)[-1] == "":
            filename += ".cfg"

        return filename

    def toogle_connection(self):

        if self._am_i_simulating:

            icon_path = pkg_resources.resource_filename(
                'samfp_gui', 'icons/connected-icon.png')

            self._am_i_simulating = False

        else:

            icon_path = pkg_resources.resource_filename(
                'samfp_gui', 'icons/disconnected-icon.png')

            self._am_i_simulating = True

        self.toogle_connect_action.setIcon(QtGui.QIcon(icon_path))


class MyCentralWidget(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        super(MyCentralWidget, self).__init__(*args, **kwargs)

        # Init bottom group
        self.scan_button = QtWidgets.QPushButton("Scan")
        self.abort_button = QtWidgets.QPushButton("Abort")
        self.progress_bar = QtWidgets.QProgressBar()

        self.bottom_group = self.init_bottom_panel()

        # Initilize left group
        self.binning = ComboBox("Image binning:", ['1', '2', '4'])
        self.obs_type = ComboBox("Observation type: ",
                                 ["DARK", "DFLAT", "OBJECT", "SFLAT", "ZERO"])
        self.target_name = TextTField("Target name:", "")
        self.comment = TextTField("Comment:", "")
        self.exp_time = FloatTField("Exposure time [s]:", 1)
        self.sleep_time = FloatTField("Sleep time [s]:", 0)
        self.n_frames = IntTField("Frames per channel:", 1)
        self.fp = ComboBox("Fabry-Perot: ",
                           ["Low-Resolution", "High-Resolution"])
        self.fp_gap_size = FloatTField("Gap size [um]:", 44)

        self.left_group = self.init_left_panel()

        # Init top group
        self.basename = TextTField("Basename", "")
        self.path = TextTField("Path:", "")

        self.top_group = self.init_top_panel()

        # Initialize right group
        self.page_scan = PageScan()
        self.page_calibration = PageCalibrationScan()
        self.page_science = PageScienceScan()

        self.notebook = QtWidgets.QTabWidget()
        self.right_group = self.init_right_panel()

        # Put all of them in the main grid
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.left_group)
        hbox.addWidget(self.right_group)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.top_group)
        vbox.addLayout(hbox)
        vbox.addWidget(self.bottom_group)

        self.setLayout(vbox)

        # Create a thread
        self.thread = QtCore.QThread()

        # Create the process object
        self.scan = Scan()
        self.scan.moveToThread(self.thread)

        # Connect thread and process object
        self.thread.started.connect(self.scan.start)
        self.thread.finished.connect(self.scan.stop)

        # Connect events to widgets
        self.connect_widgets()

    def connect_widgets(self):
        """Connect all the events to the existing widgets."""

        # Connect the start of the scan
        self.scan_button.clicked.connect(self.scan_start)

        # Connect the scan abort
        self.abort_button.clicked.connect(self.scan_abort)

        # Connect when the FP combo box change index/value
        self.fp.combo_box.currentIndexChanged.connect(self.on_fp_change)

        # Connect when we set the calibration scan pameters
        self.page_calibration.set_scanpars_button.clicked.connect(
            self.setup_calibration_scan
        )
        self.page_calibration.set_scanpars_button.clicked.connect(
            self.page_scan.set_id
        )

        # Connect when we set the science scan pameters
        self.page_science.set_scanpars_button.clicked.connect(
            self.setup_calibration_scan
        )
        self.page_science.set_scanpars_button.clicked.connect(
            self.page_scan.set_id
        )

        # self.close.connect(self.scan_abort)

        # Connect the progress bar to the signal in the scan
        self.scan.signal_value.connect(self.update_progress_bar)

        # Also connect the scan state to the buttons state
        self.scan.signal_running.connect(self.enable_scan)


    def init_bottom_panel(self):
        """Initialize the widgets at the bottom of the screen."""

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
        """Initialize the widgets at the left of the screen."""

        group = QtWidgets.QGroupBox()

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.binning.label, 0, 0)
        grid.addWidget(self.binning.combo_box, 0, 1)

        grid.addWidget(self.obs_type.label, 1, 0)
        grid.addWidget(self.obs_type.combo_box, 1, 1)

        grid.addWidget(self.target_name.label, 2, 0)
        grid.addWidget(self.target_name.line_edit, 2, 1)

        grid.addWidget(self.comment.label, 3, 0)
        grid.addWidget(self.comment.line_edit, 3, 1)

        grid.addWidget(HLine(), 4, 0, 1, 3)

        grid.addWidget(self.exp_time.label, 5, 0)
        grid.addWidget(self.exp_time.line_edit, 5, 1)

        grid.addWidget(self.n_frames.label, 6, 0)
        grid.addWidget(self.n_frames.line_edit, 6, 1)

        grid.addWidget(HLine(), 7, 0, 1, 3)

        grid.addWidget(self.fp.label, 8, 0)
        grid.addWidget(self.fp.combo_box, 8, 1)

        grid.addWidget(self.fp_gap_size.label, 9, 0)
        grid.addWidget(self.fp_gap_size.line_edit, 9, 1)
        self.fp_gap_size.disable()

        grid.setAlignment(QtCore.Qt.AlignLeft)
        grid.setAlignment(QtCore.Qt.AlignTop)
        group.setLayout(grid)

        return group

    def init_top_panel(self):

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

    def init_right_panel(self):

        self.notebook.addTab(self.page_scan, "Basic Scan")
        self.notebook.addTab(self.page_calibration, "Calibration Scan")
        self.notebook.addTab(self.page_science, "Science Scan")

        return self.notebook

    def on_fp_change(self):

        if self.fp().lower() == "low-resolution":
            self.fp_gap_size(44)
        elif self.fp().lower() == "high-resolution":
            self.fp_gap_size(200)
        else:
            self.fp_gap_size(-1)

    def scan_abort(self):

        # Just some debug levelgi
        log.debug('"Abort" buttom pressed.')

        # Gently quit the thread
        self.scan.stop()
        self.thread.quit()
        self.thread.wait()  # block until your thread as properly finished.

    def scan_start(self):

        # Just some debug level
        log.debug('"Scan" buttom pressed.')

        # Saving temporary configuration file
        main_window = self.parent()
        main_window.save_config_file(main_window.temp_cfg_file)

        # Configure the thread
        _current_page = self.notebook.currentWidget()
        self.scan.n_steps = _current_page.total_steps
        self.scan.config_file = main_window.temp_cfg_file
        self.scan.on_change_value(0)

        # Make sure that the thread has stopped
        if self.thread.isRunning():
            log.debug('There is a thread still running. Killing it.')
            self.thread.quit()
            self.thread.wait()
        else:
            log.debug('No thread running.')

        # Start the thread
        self.thread.start()

    def setup_calibration_scan(self):

        overscan_factor = self.page_calibration.overscan_factor()
        sampling = self.page_calibration.sample_factor()
        finesse = self.page_calibration.finesse()
        fwhm = self.page_calibration.fwhm()

        n_channels = overscan_factor * finesse * sampling
        z_step = fwhm / sampling

        self.page_scan.n_channels(round(n_channels))
        self.page_scan.z_step(- z_step)

    def setup_science_scan(self):

        overscan_factor = self.page_science.overscan_factor()
        sampling = self.page_science.sample_factor()

        QGC = self.page_science.queensgate_constant()
        finesse = self.page_science.finesse()

        sci_fsr = self.page_science.observed_wavelength / QGC
        sci_fwhm = finesse / sci_fsr

        n_channels = overscan_factor * finesse * sampling
        z_step = sci_fwhm / sampling

        self.page_scan.n_channels(round(n_channels))
        self.page_scan.z_step(- z_step)

    def timerEvent(self, e):

        if self.current_channel > self.total_channels:
            self.current_sweep += 1
            self.current_channel = 1
            self.z = self.z_start()

        if self.step > 100:
            self.timer.stop()
            self.scan_abort()
            return

        if self.z < 0 or self.z > 4095:
            self.timer.stop()
            self.scan_abort()

        if self.current_sweep > self.n_sweeps:
            self.timer.stop()
            self.scan_abort()

        log.info("   Sweep: {}, Channel {}, Z {}, {:03.1f} % ".format(
            self.current_sweep, self.current_channel, self.z, self.step))

        scan.set_image_basename(
            "{:s}_{:03d}".format(self.basename(), self.current_channel))

        scan.fp_moveabs(int(round(self.z)))
        scan.set_scan_current_z(int(round(self.z)))
        scan.set_scan_current_sweep(self.current_sweep)

        time.sleep(self.sleep_time())
        scan.expose()

        self.current_channel += 1
        self.z += self.z_step()

        self.step += self.step_fraction
        self.progress_bar.setValue(self.step)

    @pyqtSlot(int)
    def update_progress_bar(self, val):
        self.progress_bar.setValue(val)

    @pyqtSlot(bool)
    def enable_scan(self, val):
        self.scan_button.setDisabled(val)
        self.abort_button.setEnabled(val)
        self.progress_bar.setEnabled(val)


class Scan(QtCore.QObject):

    signal_value = QtCore.pyqtSignal(int)
    signal_running = QtCore.pyqtSignal(bool)

    def __init__(self, is_simulation=None):
        super(Scan, self).__init__()

        self.config_file = None
        self._isRunning = False
        self._isSimulation = is_simulation
        self._maxSteps = 1
        self._step = None

        self.signal_running.emit(self._isRunning)

    @property
    def n_steps(self):
        return self._maxSteps

    @n_steps.setter
    def n_steps(self, value):
        self._maxSteps = value

    def on_change_value(self, value):
        value = int(value * 100. / self._maxSteps)
        self.signal_value.emit(value)

    def start(self):
        """
        This is what happens when the scan actually starts. Any configuration
        have to be done before this is called or triggered.
        """

        log.debug("Start scan.")

        # Start scan parameters
        self._step = 0
        self._isRunning = True
        self.signal_running.emit(self._isRunning)

        # Running the scan
        if self._isSimulation:
            while (self._step < self._maxSteps) and self._isRunning:

                # Increment a step
                self._step += 1

                # Sleep simulates operations within the server
                time.sleep(1)

                # When finished, emit a signal and print it
                self.on_change_value(self._step)
                log.debug("Current scan step: %d" % self._step)

        else:
            # Read the temp configuration file
            cfg = configparser.RawConfigParser()
            cfg.read(self.config_file)

            # Parse configuration
            scan.set_image_basename(str(cfg.get('file', 'basename')))
            scan.set_image_path(str(cfg.get('file', 'path')))

            scan.set_binning(int(cfg.get('obs', 'binning')))
            scan.set_comment(str(cfg.get('obs', 'comment')))
            scan.set_image_exposure_time(cfg.getfloat('obs', 'exptime'))
            scan.set_image_nframes(cfg.getint('obs', 'nframes'))
            scan.set_target_name(str(cfg.get('obs', 'title')))
            scan.set_image_type(str(cfg.get('obs', 'type')))

            current_page_index = int(cfg.get('gui', 'active_page'))
            pages = ['scan', 'calib', 'science']
            section = pages[current_page_index]

            number_of_channels = cfg.getint(section, 'nchannels')
            number_of_sweeps = cfg.getint(section, 'nsweeps')
            z = cfg.getint(section, 'zstart')
            dz = cfg.getfloat(section, 'zstep')

            stime = 0.1

            # Prepare the scan parameters
            scan.set_scan_id()

            for sweep in range(number_of_sweeps):

                print("Moving FP to the initial Z = {:d}".format(z))
                z = scan.fp_moveabs(z)
                scan.set_scan_start(z)
                scan.set_scan_current_sweep(sweep + 1)

                for channel in range(number_of_channels):

                    z = z + dz

                    if self._isRunning is False:
                        self.stop()
                        return

                    if 4095 < z or z < 0:
                        log.warning("Z = {z:d} out of the allowed range [0, 4095]".format(z))
                        continue

                    # Increment a step
                    self._step += 1
                    self.on_change_value(self._step)

                    scan.fp_moveabs(int(round(z)))
                    scan.set_scan_current_z(int(round(z)))

                    time.sleep(stime)
                    scan.expose()

        # Leaving gracefully
        self.stop()


    def stop(self):
        """
        Stop the scan. This method can either be used to force the scan to stop
        or to make sure that the scan will be finished properly.
        """
        self._isRunning = False
        self.signal_running.emit(self._isRunning)
