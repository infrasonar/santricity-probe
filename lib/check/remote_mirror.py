from libprobe.asset import Asset
from ..query import query


async def check_remote_mirror(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/remote-mirror-pairs'
    data = await query(asset, asset_config, check_config, path)

    res = [{
        'name': item['id'],
        'label': item['base']['label'],
        'objectType': item['base']['objectType'],
        'capacity': item.get('capacity'),
        'lastCompleteTime': item.get('lastCompleteTime'),
        'status': item.get('status'),
    } for item in data]
    return {
        'remoteMirror': res
    }
