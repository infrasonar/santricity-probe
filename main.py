from libprobe.probe import Probe
from lib.check.controller import check_controller
from lib.check.disk import check_disk
from lib.check.interface import check_interface
from lib.check.santricity import check_santricity
from lib.check.volume import check_volume
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'controller': check_controller,
        'disk': check_disk,
        'interface': check_interface,
        'volume': check_volume,

        # TODO use this check or remove storageSystemId path param
        'santricity': check_santricity
    }

    probe = Probe("santricity", version, checks)

    probe.start()
