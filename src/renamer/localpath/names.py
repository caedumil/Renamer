# Copyright (c) 2021, Carlos Millett
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the Simplified BSD License.  See the LICENSE file for details.


import re


class Name():
    def __init__(self, title, country=None, year=None):
        self._title = title
        self._country = country
        self._year = year

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, name):
        self._title = name

    @property
    def country(self):
        return self._country

    @property
    def year(self):
        return self._year


def sanitize(name):
    table = {
        ord('á'): 'a',
        ord('à'): 'a',
        ord('ã'): 'a',
        ord('â'): 'a',
        ord('é'): 'e',
        ord('è'): 'e',
        ord('ẽ'): 'e',
        ord('ê'): 'e',
        ord('í'): 'i',
        ord('ì'): 'i',
        ord('ĩ'): 'i',
        ord('î'): 'i',
        ord('ó'): 'o',
        ord('ò'): 'o',
        ord('õ'): 'o',
        ord('ô'): 'o',
        ord('ú'): 'u',
        ord('ù'): 'u',
        ord('ũ'): 'u',
        ord('û'): 'u',
        ord('ç'): 'c',
        ord('ñ'): 'n',
        ord(':'): ' -',
        ord('>'): None,
        ord('<'): None,
        ord('?'): None,
        ord('!'): None,
        ord('*'): None,
        ord('#'): None,
        ord('/'): None,
        ord('\\'): None,
        ord('\''): None,
        ord('\''): None
    }
    return name.translate(table)


def parse(name):
    reSep = re.compile(r'\W+')
    reYear = re.compile(r'^[12][0-9]{3}$')
    reCountry = re.compile(r'^([A-Za-z]{2})$')
    countryCodes = [
        'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS',
        'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG',
        'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT',
        'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI',
        'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY',
        'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH',
        'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'UK',
        'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ',
        'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT',
        'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT',
        'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP',
        'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
        'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH',
        'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU',
        'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI',
        'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG',
        'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA',
        'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG',
        'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST',
        'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK',
        'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TW', 'TZ', 'UA', 'UG', 'UM',
        'US', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU',
        'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW'
    ]

    title = country = year = None
    tmp = reSep.split(name)

    for word in tmp[-2:]:
        if reYear.match(word):
            tmp.remove(word)
            year = word

        if reCountry.match(word) and word.upper() in countryCodes:
            country = word.upper()

    title = ' '.join(tmp)

    return Name(title.upper(), country, year)
