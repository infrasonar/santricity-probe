import aiohttp
import base64
import logging
from libprobe.asset import Asset
from libprobe.exceptions import IgnoreResultException


DEFAULT_HTTPS_PORT = 8443


async def query(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        path: str) -> dict:

    address = check_config.get('address')
    if not address:
        address = asset.name
    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        logging.error(f'missing credentails for {asset}')
        raise IgnoreResultException

    auth_str = base64.encodebytes(
        f'{username}:{password}'.encode()).decode().replace('\n', '')
    url = f'https://{address}:{DEFAULT_HTTPS_PORT}{path}'
    headers = {
        'authorization': f'Basic {auth_str}',
        'accept': 'application/json',
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers,
                                ssl=False) as resp:
            resp.raise_for_status()
            assert resp.status < 203, \
                f'respose returned with error: {resp.reason} ({resp.status})'

            data = await resp.json()
            return data
