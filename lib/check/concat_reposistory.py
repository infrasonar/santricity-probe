from libprobe.asset import Asset
from ..query import query


async def check_concat_repository(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/repositories/concat'
    data = await query(asset, asset_config, check_config, path)

    res = [{
        'name': item['id'],
        'aggregateCapacity': item.get('aggregateCapacity'),
        'baseObjectType': item.get('baseObjectType'),
        'lastCompleteTime': item.get('lastCompleteTime'),
        'status': item.get('status'),
        'volumeHandle': item.get('volumeHandle'),
    } for item in data]
    return {
        'concatRepository': res
    }
