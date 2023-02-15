from libprobe.asset import Asset
from ..query import query


async def check_interface(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/analysed-interface-statistics'
    data = await query(asset, asset_config, check_config, path)
    return {
        'interface': [{
            'name': item['interfaceId'],
            'averageReadOpSize': item.get('averageReadOpSize'),
            'averageWriteOpSize': item.get('averageWriteOpSize'),
            'channelErrorCounts': item.get('channelErrorCounts'),
            'combinedIOps': item.get('combinedIOps'),
            'combinedResponseTime': item.get('combinedResponseTime'),
            'combinedThroughput': item.get('combinedThroughput'),
            'otherIOps': item.get('otherIOps'),
            'queueDepthMax': item.get('queueDepthMax'),
            'queueDepthTotal': item.get('queueDepthTotal'),
            'readIOps': item.get('readIOps'),
            'readOps': item.get('readOps'),
            'readResponseTime': item.get('readResponseTime'),
            'readThroughput': item.get('readThroughput'),
            'writeIOps': item.get('writeIOps'),
            'writeOps': item.get('writeOps'),
            'writeResponseTime': item.get('writeResponseTime'),
            'writeThroughput': item.get('writeThroughput'),
        } for item in data],
    }
