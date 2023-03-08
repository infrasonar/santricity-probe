from libprobe.asset import Asset
from ..query import query
from ..utils import to_int


def to_percent_used(item: dict):
    total = to_int(item.get('totalSizeInBytes'))
    cap = to_int(item.get('capacity'))
    current_prov = to_int(item.get('currentProvisionedCapacity'))
    try:
        return (cap - current_prov) / total * 100
    except Exception:
        return


async def check_thin_volume(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/thin-volumes'
    data = await query(asset, asset_config, check_config, path)

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
