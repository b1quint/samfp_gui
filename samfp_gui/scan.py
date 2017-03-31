#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import configparser
import logging
import socket
import sys
from time import sleep

HOST = "soarhrc.ctio.noao.edu"
PORT = 8888

logging.basicConfig()
log = logging.getLogger("samfp.scan")
log.setLevel(logging.DEBUG)

def main():

    cfg = configparser.RawConfigParser()
    cfg.read("scan.ini")
    do_scan(cfg)


def do_scan(cfg):
    # Set the image properties
    set_image_basename(str(cfg.get('image', 'basename')))
    set_comment(str(cfg.get('image', 'comment')))
    set_image_path(str(cfg.get('image', 'dir')))
    set_image_type(str(cfg.get('image', 'type')))
    set_target_name(str(cfg.get('image', 'title')))

    # Set the observation properties
    set_image_exposure_time(cfg.getfloat('obs', 'exptime'))
    set_image_nframes(cfg.getint('obs', 'nframes'))

    # Prepare the scan parameters
    set_scan_id(cfg.get('scan', 'id'))

    # Actually scan
    number_of_sweeps = cfg.getint('scan', 'nsweeps')
    number_of_channels = cfg.getint('scan', 'nchannels')
    stime = cfg.getfloat('scan', 'stime')
    z = cfg.getint('scan', 'zstart')
    dz = cfg.getfloat('scan', 'zstep')

    for sweep in range(number_of_sweeps):

        print("Moving FP to the initial Z = {:d}".format(z))
        z = fp_moveabs(z)
        set_scan_start(z)
        set_scan_current_sweep(sweep)

        for channel in range(number_of_channels):
            z = z + dz
            fp_moveabs(int(round(z)))
            set_scan_current_z(int(round(z)))

            if 4095 < z or z < 0:
                log.warning(
                    "Z = {z:d} out of the allowed range [0, 4095]".format(z))

            sleep(stime)
            expose()


def expose():
    """
    Tell SAMI to trigger an exposure in the current frame or for the current
    set of images.

    Returns
    -------
    message (string) : DONE if successful.
    """
    msg = send_command("dhe expose")
    return msg


def fp_moveabs(z):
    """
    Send a command to SAMI and the SAM-FP plugin to move the FP
    to an absolute position. It has to have a value beween 0 and 4095.

    Parameters
    ----------
    z (int) : the absolute z position.

    Returns
    -------
    z (int) : the current z position if the command was received successfully.
    """
    if 4095 < z or z < 0:
        raise (ValueError,
               "z must be between 0 and 4095. Current value: {}".format(z))

    msg = send_command("fp moveabs {:d}".format(z))
    if msg.lower() != "done":
        print(msg)

    return z


def send_command(command):
    """
    Send a command to the SAM-FP server plugin at the SAMI's GUI.

    Parameters
    ----------
    command (string) : a command to be sent via TCP/IP.

    Returns
    -------
    message (string) : the response from the plugin.
    """

    global HOST
    global PORT

    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM):
        af, sock_type, proto, cannon_name, sa = res
        try:
            s = socket.socket(af, sock_type, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('Could not send command: {:s}'.format(command))
        return "ERROR"

    s.sendall(command)
    message = s.recv(1024)
    s.close()

    log.debug("{command:s} - {message:s}".format(**locals()))
    return message


def set_comment(comment):
    """
    Add a comment to the header. This will be stored in the keyword
     NOTES.

    Parameters
    ----------
    target_name (string) : any comment to be added to the FITS header.

    Returns
    -------
    message (string) : DONE if successful.
    """
    message = send_command('dhe set image.comment {:s}'.format(comment))
    return message


def set_binning(bin_size):
    """
    Set the bin size for the images. This is usually 4x4 pixels for the SAM-FP
    mode so it will be set as default.

    Parameters
    ----------
    bin_size (int) : bin size

    Returns
    -------
    message (string) : DONE if successful
    """
    binx = bin_size
    biny = bin_size
    message = send_command('sami dhe set binning {:d} {:d}'.format(binx, biny))
    return message


def set_image_basename(basename):
    """
    Set the image basename.

    Parameters
    ----------
    image_type (string) : the image type [DARK|DFLAT|OBJECT|SFLAT|ZERO]

    Returns
    -------
    message (string) : DONE if successful.
    """
    message = send_command('dhe set image.basename {:s}'.format(basename))
    return message


def set_image_exposure_time(exp_time):
    """
    Send the command to set the exposure time per frame to SAMI.

    Parameters
    ----------
    exp_time (float) : the exposure time in seconds.

    Returns
    -------
    message (string) : DONE if successful.
    """
    message = send_command("dhe set obs.exptime {:f}".format(exp_time))
    return message


def set_image_path(path):
    """
    Set the path to where the images will be saved in SAMI's computer.

    Parameters
    ----------
    path (string) : the path

    Returns
    -------
    message (string) : DONE if successful.
    """
    # TODO - Check if remote path exists
    message = send_command('dhe set image.dir {:s}'.format(path))
    return message


def set_image_nframes(nimages=1):
    """
    (re)Set the number of images that will be taken at once. For a data-cube, this
    means how many frames will be taken at each position during one sweep.

    Parameters
    ----------
    nimages (int) : the number of images that will be taked at once.

    Returns
    -------
    message (string) : DONE if successful.
    """
    message = send_command('dhe set obs.nimages {:d}'.format(nimages))
    return message


def set_image_type(image_type):
    """
    Set the image type that will be acquired.

    Parameters
    ----------
    image_type (string) : the image type [DARK|DFLAT|OBJECT|SFLAT|ZERO]

    Returns
    -------
    message (string) : DONE if successful.
    """
    options = ["DARK", "DFLAT", "OBJECT", "SFLAT", "ZERO"]

    log.debug(" Image type: {}".format(image_type))

    if image_type.upper() not in options:
        error_msg = "Image type {} ".format(image_type) + \
                    "not found within the available options"
        raise (ValueError, error_msg)

    message = send_command('dhe set image.type {:s}'.format(image_type))
    return message


def set_target_name(target_name):
    """
    Set the target name on SAMI's GUI. If the target name has any space it
    will be replaced by an underscore (_). This information will be stored
    in the FITS header within the key OBJECT.

    Parameters
    ----------
    target_name (string) : the target name

    Returns
    -------
    message (string) : DONE if successful.
    """
    target_name = target_name.replace(" ", "_")
    message = send_command('dhe set image.title {:s}'.format(target_name))
    return message


def set_scan_id(_id=None, key="FAPERSID"):
    """
    Set the scan id to be used when assembling data-cubes in the future.
    If no id is given, it creates a random one using the data and the hour.
    The keyword where the scan ID will be saved can also be changed but
    it has to be properly configured within SAMI's machine.

    Parameters
    ----------
    _id (string) : optional. If no ID is providen, one is created using the
    time "now" using the SCAN_%Y%m%d_UTC%H%M%S timestamp.

    Returns
    -------
    message (string) : DONE if successful.
        """
    if _id is None:
        from datetime import datetime
        now = datetime.utcnow()
        _id = now.strftime("SCAN_%Y%m%d_UTC%H%M%S")

    message = send_command(
        'dhe dbs set {key:s} {_id:s}'.format(**locals()))
    return message


def set_scan_nchannels(nchannels=0, key="FPNCHAN"):
    """
    Set the number of channels that a data-cube will have. This must be
    previously calculated and just inserted here.

    Parameters
    ----------
    nchannels (int) : the number of channels that the scan will have.
    key (string) : the keyword that will store this value in the header.

    Returns
    -------
    message (string) : DONE if successful.
    """
    s = "dhe dbs set {key:s} {nchannels:d}".format(**locals())
    message = send_command(s)
    return s


def set_scan_start(zstart=0, key="FPZINIT"):
    """
    Set the value where the FP will start scanning in the
    header. This is useful only to reconstruct the data-cube. It
    does not actually interfere in the scanning process.

    Parameters
    ----------
    zstart (int) : where the scan will begin
    key (string) : keyword where this will be stored

    Returns
    -------
    message (string) : DONE if successful.
    """
    s = "dhe dbs set {key:s} {zstart:f}".format(**locals())
    message = send_command(s)
    return message


def set_scan_current_sweep(sweep=0, key="FAPERSWP"):
    """
    Set the scan current sweep ID to the header to be used later.

    Parameters
    ----------
    sweep (int) : the sweep number.
    key (string) : keyword where this will be stored

    Returns
    -------
    message (string) : DONE if successful.
    """
    message = send_command('dhe dbs set {key:s} {sweep:f}'.format(**locals()))
    return message


def set_scan_current_z(z=0, key="FAPERSST"):
    """
    Set the scan current Z position in BCV.

    Parameters
    ----------
    z (int) : the current z value
    key (string) : keyword where this will be stored

    Returns
    -------
    message (string) : DONE if successful.
    """
    message = send_command('dhe dbs set {key:s} {z:d}'.format(**locals()))
    return message


if __name__ == "__main__":
    main()
