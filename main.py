from libprobe.probe import Probe
from lib.check.santricity import check_santricity
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'santricity': check_santricity
    }

    probe = Probe("santricity", version, checks)

    probe.start()
