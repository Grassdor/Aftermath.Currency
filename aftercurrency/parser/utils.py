import aiohttp
import datetime
import math

from pydantic import AnyHttpUrl

from ..config import settings


def get_current_datetime(offset: int = settings.timezone_offset, tz: bool = False) -> datetime.datetime:
    if tz:
        return datetime.datetime.now(tz=settings.get_tz())
    return datetime.datetime.utcnow() + datetime.timedelta(hours=offset)


def beautify_price(price: int | float) -> int:
    return int(math.ceil(price / 10000.0)) * 10000


async def check_availability(url: AnyHttpUrl) -> bool:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return response.status / 100 == 2
        except Exception as e:
            return False
