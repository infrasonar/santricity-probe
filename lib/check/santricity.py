from asyncsnmplib.mib.mib_index import MIB_INDEX
from asyncsnmplib.exceptions import SnmpNoAuthParams, SnmpNoConnection
from asyncsnmplib.utils import InvalidConfigException, snmp_queries
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreResultException

QUERIES = (
    MIB_INDEX['SM10-R3-MIB']['infoEntry'],
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
    return state
