import time
from libprobe.asset import Asset
from ..query import query


async def check_system(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    now = int(time.time())
    path = '/devmgr/v2/storage-systems/{ssid}/graph'
    data = await query(asset, asset_config, check_config, path)

    sa_data = data['sa']['saData']
    sa = {
        'name': sa_data['storageArrayLabel'],
        'needsAttention': sa_data.get('needsAttention'),
    }
    boot_time = sa_data.get('bootTime')
    if boot_time:
        sa['bootTime'] = int(boot_time)
        sa['uptime'] = now - int(boot_time)

    battery = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'status': item.get('status'),
        'batteryCanExpire': item.get('batteryCanExpire'),
        'automaticAgeReset': item.get('automaticAgeReset'),
        'vendorName': item.get('vendorName'),
        'vendorPN': item.get('vendorPN'),
    } for item in data['componentBundle']['battery']]

    esm = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'status': item.get('status'),
        'productID': item.get('productID'),
        'partNumber': item.get('partNumber'),
        'serialNumber': item.get('serialNumber'),
    } for item in data['componentBundle']['esm']]

    fan = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'status': item.get('status'),
    } for item in data['componentBundle']['fan']]

    power_supply = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'status': item.get('status'),
        'partNumber': item.get('partNumber'),
        'serialNumber': item.get('serialNumber'),
    } for item in data['componentBundle']['powerSupply']]

    thermal_sensor = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'parentCruType': item['rtrAttributes']['parentCru']['type'],
        'status': item.get('status'),
    } for item in data['componentBundle']['thermalSensor']]

    tray = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'drvMHSpeedMismatch': item.get('drvMHSpeedMismatch'),
        'esmFactoryDefaultsMismatch': item.get('esmFactoryDefaultsMismatch'),
        'esmHardwareMismatch': item.get('esmHardwareMismatch'),
        'esmMiswire': item.get('esmMiswire'),
        'esmVersionMismatch': item.get('esmVersionMismatch'),
        'isMisconfigured': item.get('isMisconfigured'),
        'partNumber': item.get('partNumber'),
        'serialNumber': item.get('serialNumber'),
        'trayIDConflict': item.get('trayIDConflict'),
        'trayIDMismatch': item.get('trayIDMismatch'),
        'unsupportedTray': item.get('unsupportedTray'),
    } for item in data['tray']]

    return {
        'array': [sa],
        'battery': battery,
        'esm': esm,
        'fan': fan,
        'powerSupply': power_supply,
        'thermalSensor': thermal_sensor,
        'tray': tray,
    }
