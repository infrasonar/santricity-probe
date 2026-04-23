from libprobe.asset import Asset
from libprobe.check import Check
from ..query import query
from ..utils import to_int


def to_percent_used(item: dict):
    total = to_int(item.get('totalSizeInBytes'))
    cap = to_int(item.get('capacity'))
    current_prov = to_int(item.get('currentProvisionedCapacity'))
    try:
        assert isinstance(total, int)
        assert isinstance(cap, int)
        assert isinstance(current_prov, int)
        return (cap - current_prov) / total * 100
    except Exception:
        return


class CheckThinVolume(Check):
    key = 'thinVolume'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        path = '/devmgr/v2/storage-systems/{ssid}/thin-volumes'
        data = await query(asset, local_config, config, path)

        res = [{
            'name': item['label'],
            'capacity': to_int(item.get('capacity')),
            'currentProvisionedCapacity':
                to_int(item.get('currentProvisionedCapacity')),
            'initialProvisionedCapacity':
                to_int(item.get('initialProvisionedCapacity')),
            'percentUsed': to_percent_used(item),
            'totalSizeInBytes': to_int(item.get('totalSizeInBytes')),
        } for item in data]
        return {
            'thinVolume': res
        }
