from libprobe.asset import Asset
from ..query import query


async def check_thin_volume(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/thin-volumes'
    data = await query(asset, asset_config, check_config, path)

    res = [{
        'name': item['label'],
        'capacity': item.get('capacity'),
        'currentProvisionedCapacity': item.get('currentProvisionedCapacity'),
        'initialProvisionedCapacity': item.get('initialProvisionedCapacity'),
        'totalSizeInBytes': item.get('totalSizeInBytes'),
    } for item in data]
    return {
        'thinVolume': res
    }
