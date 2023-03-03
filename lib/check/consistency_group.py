from libprobe.asset import Asset
from ..query import query


async def check_consistency_group(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/consistency-groups'
    data = await query(asset, asset_config, check_config, path)

    res = [{
        'name': item['id'],
        'autoDeleteLimit': item.get('autoDeleteLimit'),
        'creationPendingStatus': item.get('creationPendingStatus'),
        'fullWarnThreshold': item.get('fullWarnThreshold'),
        'label': item.get('label'),
        'repFullPolicy': item.get('repFullPolicy'),
    } for item in data]
    return {
        'consistencyGroup': res
    }
