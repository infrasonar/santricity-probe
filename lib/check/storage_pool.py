from libprobe.asset import Asset
from ..query import query
from ..utils import to_int


def to_percent_used(item: dict):
    total = to_int(item.get('totalRaidedSpace'))
    used = to_int(item.get('usedSpace'))
    try:
        return used / total * 100  # type: ignore
    except Exception:
        return


async def check_storage_pool(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/storage-pools'
    data = await query(asset, asset_config, check_config, path)

    res = [{
        'name': item['label'],
        'diskPool': item.get('diskPool'),
        'freeSpace': to_int(item.get('freeSpace')),
        'raidStatus': item.get('raidStatus'),
        'percentUsed': to_percent_used(item),
        'totalRaidedSpace': to_int(item.get('totalRaidedSpace')),
        'usedSpace': to_int(item.get('usedSpace')),
    } for item in data]
    return {
        'storagePool': res
    }
