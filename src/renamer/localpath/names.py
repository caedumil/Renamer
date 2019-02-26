# Copyright (c) 2014 - 2018, Carlos Millett
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

    @property
    def country(self):
        return self._country

    @property
    def year(self):
        return self._year

    def combiantions(self):
        combinations = [self._title]

        if self._country:
            combinations.append('{} {}'.format(self._title, self._country))

        if self._year:
            tmp = []
            for cmb in combinations:
                tmp.append('{} {}'.format(cmb, self._year))
            combinations.extend(tmp)

        return combinations


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
    reSep = re.compile(r'[\W]+')
    reYear = re.compile('[12][0-9]{3}')
    reCountry = re.compile(r'[\W]([A-Z]{2})[\W]?')
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

    nameOnly = country = year = None
    tmp = name

    if reCountry.search(name):
        match = reCountry.findall(name)[0]

        if match in countryCodes:
            country = 'GB' if match == 'UK' else match
            tmp = reCountry.sub('', name)

    if reYear.search(name):
        match = reYear.findall(name)
        year = match[0]

    nameOnly = reSep.sub(' ', reYear.sub('', tmp)).strip()

    return Name(nameOnly.title(), country, year)
