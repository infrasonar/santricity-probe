import time
from libprobe.asset import Asset
from libprobe.check import Check
from ..query import query


class CheckController(Check):
    key = 'controller'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        now = int(time.time())  # TODO move this down?
        path = \
            '/devmgr/v2/storage-systems/{ssid}/analysed-controller-statistics'
        data = await query(asset, local_config, config, path)
        statistics = {
            item['controllerId']: {
                'averageReadOpSize': item.get('averageReadOpSize'),
                'averageWriteOpSize': item.get('averageWriteOpSize'),
                'combinedIOps': item.get('combinedIOps'),
                'combinedResponseTime': item.get('combinedResponseTime'),
                'combinedThroughput': item.get('combinedThroughput'),
                'cpuAvgUtilization': item.get('cpuAvgUtilization'),
                'cpuAvgUtilizationPerCore':
                    item.get('cpuAvgUtilizationPerCore'),
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
        data = await query(asset, local_config, config, path)

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
