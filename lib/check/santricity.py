from libprobe.asset import Asset
from ..query import query


async def check_santricity(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems'
    data = await query(asset, asset_config, check_config, path)
    return {
        'storageSystems': [{
            'name': item['id'],
            'systemName': item.get('name'),
            'systemId': item.get('wwn'),
        } for item in data],
    }
