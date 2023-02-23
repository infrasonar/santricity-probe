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
        } for item in data
    }

    path = '/devmgr/v2/storage-systems/{ssid}/drives'
    data = await query(asset, asset_config, check_config, path)

    output = []
    for item in data:
        disk = {
            'name': item['physicalLocation']['label'],
            'available': item.get('available'),
            'blkSize': item.get('blkSize'),
            'blkSizePhysical': item.get('blkSizePhysical'),
            'cause': item.get('cause'),
            'currentCommandAgingTimeout':
            item.get('currentCommandAgingTimeout'),
            'currentSpeed': item.get('currentSpeed'),
            'currentVolumeGroupRef': item.get('currentVolumeGroupRef'),
            'defaultCommandAgingTimeout':
            item.get('defaultCommandAgingTimeout'),
            'driveMediaType': item.get('driveMediaType'),
            'driveRef': item.get('driveRef'),
            'fdeCapable': item.get('fdeCapable'),
            'fdeEnabled': item.get('fdeEnabled'),
            'fdeLocked': item.get('fdeLocked'),
            'fipsCapable': item.get('fipsCapable'),
            'firmwareVersion': item.get('firmwareVersion'),
            'fpgaVersion': item.get('fpgaVersion'),
            'hasDegradedChannel': item.get('hasDegradedChannel'),
            'hotSpare': item.get('hotSpare'),
            'id': item.get('id'),
            'interposerPresent': item.get('interposerPresent'),
            'interposerRef': item.get('interposerRef'),
            'invalidDriveData': item.get('invalidDriveData'),
            'locateInProgress': item.get('locateInProgress'),
            'lockKeyID': item.get('lockKeyID'),
            'lockKeyIDValue': item.get('lockKeyIDValue'),
            'lowestAlignedLBA': item.get('lowestAlignedLBA'),
            'manufacturer': item.get('manufacturer'),
            'manufacturerDate': item.get('manufacturerDate'),
            'maxSpeed': item.get('maxSpeed'),
            'mirrorDrive': item.get('mirrorDrive'),
            'nonRedundantAccess': item.get('nonRedundantAccess'),
            'offline': item.get('offline'),
            'pfa': item.get('pfa'),
            'pfaReason': item.get('pfaReason'),
            'phyDriveType': item.get('phyDriveType'),
            'productID': item.get('productID'),
            'protectionInformationCapable':
            item.get('protectionInformationCapable'),
            'protectionType': item.get('protectionType'),
            'rawCapacity': item.get('rawCapacity'),
            'removed': item.get('removed'),
            'reserved': item.get('reserved'),
            'serialNumber': item.get('serialNumber'),
            'softwareVersion': item.get('softwareVersion'),
            'sparedForDriveRef': item.get('sparedForDriveRef'),
            'spindleSpeed': item.get('spindleSpeed'),
            'status': item.get('status'),
            'uncertified': item.get('uncertified'),
            'usableCapacity': item.get('usableCapacity'),
            'volumeGroupIndex': item.get('volumeGroupIndex'),
            'workingChannel': item.get('workingChannel'),
            'worldWideName': item.get('worldWideName'),
        }
        perf = statistics.get(item['id'])
        if perf:
            disk.update(perf)

        output.append(disk)

    return output
