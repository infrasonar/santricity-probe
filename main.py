from libprobe.probe import Probe
from lib.check.drive import check_drive
from lib.check.interface import check_interface
from lib.check.santricity import check_santricity
from lib.check.system import check_system
from lib.check.volume import check_volume
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'drive': check_drive,
        'interface': check_interface,
        'system': check_system,
        'volume': check_volume,

        # TODO use this check or remove storageSystemId path param
        'santricity': check_santricity
    }

    probe = Probe("santricity", version, checks)

    probe.start()
