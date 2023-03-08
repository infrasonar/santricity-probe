from libprobe.asset import Asset
from ..query import query


async def check_disk(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/analysed-drive-statistics'
    data = await query(asset, asset_config, check_config, path)
    statistics = {
        item['diskId']: {
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
        } for item in data
    }

    path = '/devmgr/v2/storage-systems/{ssid}/storage-pools'
    data = await query(asset, asset_config, check_config, path)
    storage_pools = {item['id']: item for item in data}

    path = '/devmgr/v2/storage-systems/{ssid}/drives'
    data = await query(asset, asset_config, check_config, path)

    output = []
    for item in data:
        disk = {
            'name': item['physicalLocation']['label'],
            'driveMediaType': item.get('driveMediaType'),
            'productID': item.get('productID'),
            'status': item.get('status'),
            'currentTemp': item.get('driveTemperature', {}).get('currentTemp'),
            'refTemp': item.get('driveTemperature', {}).get('refTemp'),
            'averageEraseCountPercent':
            item.get('ssdWearLife', {}).get('averageEraseCountPercent'),
            'spareBlocksRemainingPercent':
            item.get('ssdWearLife', {}).get('spareBlocksRemainingPercent'),

        }
        storage_pool = storage_pools.get(item['currentVolumeGroupRef'])
        if storage_pool:
            disk['volumeGroup'] = storage_pool.get('label')

        perf = statistics.get(item['id'])
        if perf:
            disk.update(perf)

        output.append(disk)

    return {
        'disk': output
    }
