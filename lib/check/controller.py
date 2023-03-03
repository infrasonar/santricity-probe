from libprobe.asset import Asset
from ..query import query


async def check_controller(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/analysed-controller-statistics'
    data = await query(asset, asset_config, check_config, path)
    statistics = {
        item['controllerId']: {
            'averageReadOpSize': item.get('averageReadOpSize'),
            'averageWriteOpSize': item.get('averageWriteOpSize'),
            'combinedIOps': item.get('combinedIOps'),
            'combinedResponseTime': item.get('combinedResponseTime'),
            'combinedThroughput': item.get('combinedThroughput'),
            'cpuAvgUtilization': item.get('cpuAvgUtilization'),
            'cpuAvgUtilizationPerCore': item.get('cpuAvgUtilizationPerCore'),
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

    path = '/devmgr/v2/storage-systems/{ssid}/controllers'
    data = await query(asset, asset_config, check_config, path)

    output = []
    for item in data:
        controller = {
            'name': item['physicalLocation']['label'],
            'active': item.get('active'),
            'appVersion': item.get('appVersion'),
            'boardID': item.get('boardID'),
            'boardSubmodelID': item.get('boardSubmodelID'),
            'bootTime': item.get('bootTime'),
            'bootVersion': item.get('bootVersion'),
            'cacheMemorySize': item.get('cacheMemorySize'),
            'controllerErrorMode': item.get('controllerErrorMode'),
            'controllerRef': item.get('controllerRef'),
            'flashCacheMemorySize': item.get('flashCacheMemorySize'),
            'hasTrayIdentityIndicator': item.get('hasTrayIdentityIndicator'),
            'hostBoardID': item.get('hostBoardID'),
            'id': item.get('id'),
            'locateInProgress': item.get('locateInProgress'),
            'manufacturer': item.get('manufacturer'),
            'manufacturerDate': item.get('manufacturerDate'),
            'modelName': item.get('modelName'),
            'oemPartNumber': item.get('oemPartNumber'),
            'partNumber': item.get('partNumber'),
            'physicalCacheMemorySize': item.get('physicalCacheMemorySize'),
            'processorMemorySize': item.get('processorMemorySize'),
            'productID': item.get('productID'),
            'productRevLevel': item.get('productRevLevel'),
            'quiesced': item.get('quiesced'),
            'readyToRemove': item.get('readyToRemove'),
            'reserved1': item.get('reserved1'),
            'reserved2': item.get('reserved2'),
            'serialNumber': item.get('serialNumber'),
            'status': item.get('status'),
            'submodelSupported': item.get('submodelSupported'),
        }
        perf = statistics.get(item['id'])
        if perf:
            controller.update(perf)

        output.append(controller)

    return {
        'controller': output
    }
