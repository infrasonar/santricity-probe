from libprobe.asset import Asset
from ..query import query


async def check_storage_pool(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/storage-pools'
    data = await query(asset, asset_config, check_config, path)

    res = [{
        'name': item['label'],
        'diskPool': item.get('diskPool'),
        'freeSpace': item.get('freeSpace'),
        'raidStatus': item.get('raidStatus'),
        'totalRaidedSpace': item.get('totalRaidedSpace'),
        'usedSpace': item.get('usedSpace'),
    } for item in data]
    return {
        'storagePool': res
    }
