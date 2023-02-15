from libprobe.asset import Asset
from ..query import query


async def check_system(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/{ssid}/analysed-system-statistics'
    data = await query(asset, asset_config, check_config, path)
    return {
        'system': [{
            'name': 'system',
            'maxCpuUtilization': item.get('maxCpuUtilization'),
            'cpuAvgUtilization': item.get('cpuAvgUtilization'),
        } for item in data],
    }
