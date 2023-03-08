import time
from libprobe.asset import Asset
from ..query import query


async def check_controller(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    now = int(time.time())
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
            'status': item.get('status'),
        }
        boot_time = item.get('bootTime')
        if boot_time:
            controller['bootTime'] = int(boot_time)
            controller['uptime'] = now - int(boot_time)

        perf = statistics.get(item['id'])
        if perf:
            controller.update(perf)

        output.append(controller)

    return {
        'controller': output
    }
