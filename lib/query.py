import aiohttp
import base64
import logging
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from . import DOCS_URL
from .connector import get_connector


DEFAULT_HTTPS_PORT = 8443
DEFAULT_SSID = 1


async def query(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        path: str) -> dict:

    address = check_config.get('address')
    if not address:
        address = asset.name
    port = check_config.get('port', DEFAULT_HTTPS_PORT)
    ssid = check_config.get('storageSystemId', DEFAULT_SSID)

    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        raise CheckException(
            'Missing credentials. Please refer to the following documentation'
            f' for detailed instructions: <{DOCS_URL}>'
        )

    auth_str = base64.encodebytes(
        f'{username}:{password}'.encode()).decode().replace('\n', '')
    url = f'https://{address}:{port}{path.format(ssid=ssid)}'
    headers = {
        'authorization': f'Basic {auth_str}',
        'accept': 'application/json',
    }

    async with aiohttp.ClientSession(connector=get_connector()) as session:
        async with session.get(url,
                               headers=headers,
                               ssl=False) as resp:
            assert resp.status < 203, \
                f'respose returned with error: {resp.reason} ({resp.status})'

            data = await resp.json()
            return data
