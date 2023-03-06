from libprobe.probe import Probe
from lib.check.controller import check_controller
from lib.check.disk import check_disk
from lib.check.storage_pool import check_storage_pool
from lib.check.system import check_system
from lib.check.thin_volume import check_thin_volume
from lib.check.volume import check_volume
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'controller': check_controller,
        'disk': check_disk,
        'storagePool': check_storage_pool,
        'system': check_system,
        'thinVolume': check_thin_volume,
        'volume': check_volume,
    }

    probe = Probe("santricity", version, checks)

    probe.start()
