from libprobe.asset import Asset
from ..query import query


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
            'name': item['name'],
            'action': item.get('action'),
            'applicationTagOwned': item.get('applicationTagOwned'),
            'asyncMirrorSource': item.get('asyncMirrorSource'),
            'asyncMirrorTarget': item.get('asyncMirrorTarget'),
            'blkSize': item.get('blkSize'),
            'cacheMirroringValidateProtectionInformation':
            item.get('cacheMirroringValidateProtectionInformation'),
            'capacity': item.get('capacity'),  # TODOK int?
            'currentControllerId': item.get('currentControllerId'),
            'currentManager': item.get('currentManager'),
            'dataAssurance': item.get('dataAssurance'),
            'diskPool': item.get('diskPool'),
            'dssMaxSegmentSize': item.get('dssMaxSegmentSize'),
            'dssPreallocEnabled': item.get('dssPreallocEnabled'),
            'expectedProtectionInformationAppTag':
            item.get('expectedProtectionInformationAppTag'),
            'extendedUniqueIdentifier': item.get('extendedUniqueIdentifier'),
            'extremeProtection': item.get('extremeProtection'),
            'flashCached': item.get('flashCached'),
            'id': item.get('id'),
            'increasingBy': item.get('increasingBy'),
            'label': item.get('label'),
            'mapped': item.get('mapped'),
            'mgmtClientAttribute': item.get('mgmtClientAttribute'),
            'name': item.get('name'),
            'objectType': item.get('objectType'),
            'offline': item.get('offline'),
            'onlineVolumeCopy': item.get('onlineVolumeCopy'),
            'pitBaseVolume': item.get('pitBaseVolume'),
            'preReadRedundancyCheckEnabled':
            item.get('preReadRedundancyCheckEnabled'),
            'preferredControllerId': item.get('preferredControllerId'),
            'preferredManager': item.get('preferredManager'),
            'protectionInformationCapable':
            item.get('protectionInformationCapable'),
            'protectionType': item.get('protectionType'),
            'raidLevel': item.get('raidLevel'),
            'reconPriority': item.get('reconPriority'),
            'remoteMirrorSource': item.get('remoteMirrorSource'),
            'remoteMirrorTarget': item.get('remoteMirrorTarget'),
            'repairedBlockCount': item.get('repairedBlockCount'),
            'sectorOffset': item.get('sectorOffset'),
            'segmentSize': item.get('segmentSize'),
            'status': item.get('status'),
            'thinProvisioned': item.get('thinProvisioned'),
            'totalSizeInBytes': item.get('totalSizeInBytes'),
            'volumeCopySource': item.get('volumeCopySource'),
            'volumeCopyTarget': item.get('volumeCopyTarget'),
            'volumeFull': item.get('volumeFull'),
            'volumeGroupRef': item.get('volumeGroupRef'),
            'volumeHandle': item.get('volumeHandle'),
            'volumeRef': item.get('volumeRef'),
            'volumeUse': item.get('volumeUse'),
            'worldWideName': item.get('worldWideName'),
            'wwn': item.get('wwn'),
        }

        for m in item['listOfMappings']:
            if m['volumeRef'] == item['id']:
                volume['lun'] = m.get('lun')
                host_group = host_groups.get(m['mapRef'])
                if host_group:
                    volume['cluster'] = host_group.get('name')

        storage_pool = storage_pools.get(item['volumeGroupRef'])
        if storage_pool:
            volume['pool'] = storage_pool.get('name')

        perf = statistics.get(item['id'])
        if perf:
            volume.update(perf)

        output.append(volume)

    return {
        'volume': output
    }
