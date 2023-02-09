from asyncsnmplib.mib.mib_index import MIB_INDEX
from asyncsnmplib.exceptions import SnmpNoAuthParams, SnmpNoConnection
from asyncsnmplib.utils import InvalidConfigException, snmp_queries
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreResultException

QUERIES = (
    MIB_INDEX['UBNT-UniFi-MIB']['santricityApSystem'],
    MIB_INDEX['UBNT-UniFi-MIB']['santricityRadioEntry'],
    MIB_INDEX['UBNT-UniFi-MIB']['santricityVapEntry'],
)


async def check_santricity(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    address = check_config.get('address')
    if address is None:
        address = asset.name
    try:
        state = await snmp_queries(address, asset_config, QUERIES)
    except SnmpNoConnection:
        raise CheckException('unable to connect')
    except (InvalidConfigException, SnmpNoAuthParams):
        raise IgnoreResultException
    except Exception:
        raise
    for item in state.get('santricityRadioEntry', []):
        item.pop('santricityRadioIndex')
        item['name'] = item.pop('santricityRadioName')
    for item in state.get('santricityVapEntry', []):
        item.pop('santricityVapIndex')
        item['name'] = item.pop('santricityVapName')
    return state
