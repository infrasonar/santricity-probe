from libprobe.asset import Asset
from ..query import query


async def check_volume(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/analysed-volume-statistics'
    data = await query(asset, asset_config, check_config, path)
    return {
        'volume': [{
            'name': item['volumeName'],
            'averageReadOpSize': item.get('averageReadOpSize'),
            'averageWriteOpSize': item.get('averageWriteOpSize'),
            'combinedIOps': item.get('combinedIOps'),
            'combinedResponseTime': item.get('combinedResponseTime'),
            'combinedThroughput': item.get('combinedThroughput'),
            'flashCacheHitPct': item.get('flashCacheHitPct'),
            'flashCacheReadHitBytes': item.get('flashCacheReadHitBytes'),
            'flashCacheReadHitOps': item.get('flashCacheReadHitOps'),
            'flashCacheReadResponseTime':
                item.get('flashCacheReadResponseTime'),
            'flashCacheReadThroughput': item.get('flashCacheReadThroughput'),
            'otherIOps': item.get('otherIOps'),
            'queueDepthMax': item.get('queueDepthMax'),
            'queueDepthTotal': item.get('queueDepthTotal'),
            'readCacheUtilization': item.get('readCacheUtilization'),
            'readHitBytes': item.get('readHitBytes'),
            'readHitOps': item.get('readHitOps'),
            'readIOps': item.get('readIOps'),
            'readOps': item.get('readOps'),
            'readPhysicalIOps': item.get('readPhysicalIOps'),
            'readResponseTime': item.get('readResponseTime'),
            'readThroughput': item.get('readThroughput'),
            'writeCacheUtilization': item.get('writeCacheUtilization'),
            'writeHitBytes': item.get('writeHitBytes'),
            'writeHitOps': item.get('writeHitOps'),
            'writeIOps': item.get('writeIOps'),
            'writeOps': item.get('writeOps'),
            'writePhysicalIOps': item.get('writePhysicalIOps'),
            'writeResponseTime': item.get('writeResponseTime'),
            'writeThroughput': item.get('writeThroughput'),
        } for item in data],
    }
