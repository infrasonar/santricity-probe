from libprobe.asset import Asset
from ..query import query


async def check_disk(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/analysed-drive-statistics'
    data = await query(asset, asset_config, check_config, path)
    return {
        'disk': [{
            'name': item['diskId'],
            'averageReadOpSize': item.get('averageReadOpSize'),
            'averageWriteOpSize': item.get('averageWriteOpSize'),
            'combinedIOps': item.get('combinedIOps'),
            'combinedResponseTime': item.get('combinedResponseTime'),
            'combinedThroughput': item.get('combinedThroughput'),
            'otherIOps': item.get('otherIOps'),
            'readIOps': item.get('readIOps'),
            'readOps': item.get('readOps'),
            'readPhysicalIOps': item.get('readPhysicalIOps'),
            'readResponseTime': item.get('readResponseTime'),
            'readThroughput': item.get('readThroughput'),
            'writeIOps': item.get('writeIOps'),
            'writeOps': item.get('writeOps'),
            'writePhysicalIOps': item.get('writePhysicalIOps'),
            'writeResponseTime': item.get('writeResponseTime'),
            'writeThroughput': item.get('writeThroughput'),
        } for item in data],
    }
