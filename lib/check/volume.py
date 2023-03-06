from libprobe.asset import Asset
from ..query import query
from ..utils import to_int


async def check_volume(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/analysed-volume-statistics'
    data = await query(asset, asset_config, check_config, path)
    statistics = {
        item['volumeId']: {
            'averageReadOpSize': item.get('averageReadOpSize'),
            'averageWriteOpSize': item.get('averageWriteOpSize'),
            'combinedIOps': item.get('combinedIOps'),
            'combinedResponseTime': item.get('combinedResponseTime'),
            'combinedThroughput': item.get('combinedThroughput'),
            'controllerId': item.get('controllerId'),
            'flashCacheHitPct': item.get('flashCacheHitPct'),
            'flashCacheReadHitBytes': item.get('flashCacheReadHitBytes'),
            'flashCacheReadHitOps': item.get('flashCacheReadHitOps'),
            'flashCacheReadResponseTime':
                item.get('flashCacheReadResponseTime'),
            'flashCacheReadThroughput': item.get('flashCacheReadThroughput'),
            'mapped': item.get('mapped'),
            'otherIOps': item.get('otherIOps'),
            'poolId': item.get('poolId'),
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
            'volumeName': item.get('volumeName'),
            'workLoadId': item.get('workLoadId'),
            'writeCacheUtilization': item.get('writeCacheUtilization'),
            'writeHitBytes': item.get('writeHitBytes'),
            'writeHitOps': item.get('writeHitOps'),
            'writeIOps': item.get('writeIOps'),
            'writeOps': item.get('writeOps'),
            'writePhysicalIOps': item.get('writePhysicalIOps'),
            'writeResponseTime': item.get('writeResponseTime'),
            'writeThroughput': item.get('writeThroughput'),
        } for item in data
    }

    path = '/devmgr/v2/storage-systems/{ssid}/host-groups'
    data = await query(asset, asset_config, check_config, path)
    host_groups = {item['id']: item for item in data}

    path = '/devmgr/v2/storage-systems/{ssid}/storage-pools'
    data = await query(asset, asset_config, check_config, path)
    storage_pools = {item['id']: item for item in data}

    path = '/devmgr/v2/storage-systems/{ssid}/volumes'
    data = await query(asset, asset_config, check_config, path)

    output = []
    for item in data:
        volume = {
            'name': item['label'],
            'diskPool': item.get('diskPool'),
            'status': item.get('status'),
            'totalSizeInBytes': to_int(item.get('totalSizeInBytes')),
            'volumeUse': item.get('volumeUse'),
        }

        for m in item['listOfMappings']:
            if m['volumeRef'] == item['id']:
                volume['lun'] = m.get('lun')
                host_group = host_groups.get(m['mapRef'])
                if host_group:
                    volume['cluster'] = host_group.get('name')

        storage_pool = storage_pools.get(item['volumeGroupRef'])
        if storage_pool:
            volume['pool'] = storage_pool.get('label')

        perf = statistics.get(item['id'])
        if perf:
            volume.update(perf)

        output.append(volume)

    return {
        'volume': output
    }
