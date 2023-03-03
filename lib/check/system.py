from libprobe.asset import Asset
from ..query import query


async def check_system(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    path = '/devmgr/v2/storage-systems/{ssid}/graph'
    data = await query(asset, asset_config, check_config, path)

    battery = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        # 'label': item['physicalLocation']['label'],
        'status': item.get('status'),
        'batteryCanExpire': item.get('batteryCanExpire'),
        'automaticAgeReset': item.get('automaticAgeReset'),
        'vendorName': item.get('vendorName'),
        'vendorPN': item.get('vendorPN'),
        'manufacturerDate': item.get('manufacturerDate'),
    } for item in data['componentBundle']['battery']]

    esm = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        'label': item['physicalLocation']['label'],
        'status': item.get('status'),
        'productID': item.get('productID'),
        'partNumber': item.get('partNumber'),
        'serialNumber': item.get('serialNumber'),
        'manufacturerDate': item.get('manufacturerDate'),
    } for item in data['componentBundle']['esm']]

    fan = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        # 'label': item['physicalLocation']['label'],
        'status': item.get('status'),
    } for item in data['componentBundle']['fan']]

    power_supply = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        # 'label': item['physicalLocation']['label'],
        'status': item.get('status'),
        'partNumber': item.get('partNumber'),
        'serialNumber': item.get('serialNumber'),
        'manufacturerDate': item.get('manufacturerDate'),
    } for item in data['componentBundle']['powerSupply']]

    thermal_sensor = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        # 'label': item['physicalLocation']['label'],
        'parentCruType': item['rtrAttributes']['parentCru']['type'],
        'status': item.get('status'),
    } for item in data['componentBundle']['thermalSensor']]

    tray = [{
        'name': item['id'],
        'slot': item['physicalLocation']['slot'],
        # 'label': item['physicalLocation']['label'],
        'status': item.get('status'),
        'partNumber': item.get('partNumber'),
        'serialNumber': item.get('serialNumber'),
        'manufacturerDate': item.get('manufacturerDate'),
    } for item in data['tray']]

    return {
        'battery': battery,
        'esm': esm,
        'fan': fan,
        'powerSupply': power_supply,
        'thermalSensor': thermal_sensor,
        'tray': tray,
    }
