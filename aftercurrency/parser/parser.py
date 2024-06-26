import math
import xml.etree.ElementTree as ETree

import aiohttp

from .currency import Code
from .utils import get_current_datetime


class CBRParser:
    def __init__(self):
        self.URL: str = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx'
        self.headers: dict = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'http://web.cbr.ru/GetCursOnDate'
        }
        self.envelope = None

    def __set_envelope(self):
        self.envelope: str = '''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <GetCursOnDate xmlns="http://web.cbr.ru/">
              <On_date>{}</On_date>
            </GetCursOnDate>
          </soap:Body>
        </soap:Envelope>'''.format(get_current_datetime().date())

    async def get_rate(self, from_currency: Code, to_currency: Code | None = None) -> float | None:
        self.__set_envelope()
        rate = None
        async with aiohttp.ClientSession() as session:
            async with session.post(self.URL, headers=self.headers, data=self.envelope) as response:
                if response.status == 200:
                    xml_string = await response.text()
                    root = ETree.fromstring(xml_string)
                    if from_currency != Code.RUB:
                        for val in root.findall('.//ValuteCursOnDate'):
                            vch_code = val.find('VchCode').text.strip()
                            if vch_code == from_currency:
                                rate = float(val.find('Vcurs').text.strip())
                                break
                    else:
                        rate = 1
                    if to_currency != Code.RUB:
                        for val in root.findall('.//ValuteCursOnDate'):
                            vch_code = val.find('VchCode').text.strip()
                            if vch_code == to_currency:
                                rate_to = float(val.find('Vcurs').text.strip())
                                break
                        if rate_to:
                            rate /= rate_to
                        else:
                            rate = None
        return rate
