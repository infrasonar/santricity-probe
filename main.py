from libprobe.probe import Probe
from lib.check.controller import CheckController
from lib.check.disk import CheckDisk
from lib.check.storage_pool import CheckStoragePool
from lib.check.system import CheckSystem
from lib.check.thin_volume import CheckThinVolume
from lib.check.volume import CheckVolume
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckController,
        CheckDisk,
        CheckStoragePool,
        CheckSystem,
        CheckThinVolume,
        CheckVolume,
    )

    probe = Probe("santricity", version, checks)

    probe.start()
