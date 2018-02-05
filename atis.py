#!/usr/bin/env python
"""
ATIS Maker generates a an atis line to be used in Euroscope vatsim.net
Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of ATIS Maker.

ATIS Maker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

ATIS Maker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ATIS Maker.  If not, see <http://www.gnu.org/licenses/>.
"""
import collections
import bisect
from string import Template
from metar import Metar

default = {
    'fragments': {

        ###
        ### Fragments in here are to be replaced by airport specific files
        ###
        ### although, any of the fragments can effectively be replace by airport
        ### specific files, these are the ones that simply have no default option
        ###
        'ident': '', ## filename for '<name of airport>'
        'info': '', ## filename for 'This <name of airport> information'

        ###
        ### Approach types
        ###
        'ils': 'expect ils', ## filename for 'expect ILS approach'
        'rnav': 'expect rnav', ## filename for 'expect RNAV approach'
        'vor': 'expect vor', ## filename for 'expect VOR DME approach'
        'ndb': 'expect ndb', ## filename for 'expect NDB approach'
        'visual': 'expect visual', ## filename for 'expect visual approach'

        'runway_in_use': 'runway in use', ## filename for 'runway in use'

        'transition_level': 'transition level', ## filename for 'transition level'

        'end': 'endof', ## filename for 'end of'
        'atis': 'atis' ## filename for 'atis'
    },
    'format': '[info]lettermetar.time[approach_type][runway_in_use]arrrwy[transition_level]airport.tametar.windsmetar.temperaturesmetar.pressure[end][ident][atis]letter',
    'transition_level_table': {
        '4000': [
            (942.1, '75'),
            (959.4, '70'),
            (977.1, '65'),
            (995.0, '60'),
            (1013.2, '55'),
            (1031.6, '50'),
            (1050.3, '45'),
            (9999, '40')
        ],
        '5000': [
            (942.1, '85'),
            (959.4, '80'),
            (977.1, '75'),
            (995.0, '70'),
            (1013.2, '65'),
            (1031.6, '60'),
            (1050.3, '55'),
            (9999, '50')
        ],
        '6000': [
            (942.1, '95'),
            (959.4, '90'),
            (977.1, '85'),
            (995.0, '80'),
            (1013.2, '75'),
            (1031.6, '70'),
            (1050.3, '65'),
            (9999, '60')
        ],
        '8000': [
            (942.1, '115'),
            (959.4, '110'),
            (977.1, '105'),
            (995.0, '100'),
            (1013.2, '95'),
            (1031.6, '90'),
            (1050.3, '85'),
            (9999, '80')
        ]
    }
}

airports = {
    'LPPT': {
        'fragments': {

            ###
            ### Fragments we need to specify
            ###
            'ident': 'LPPT', ## filename for 'Lisboa'
            'info': 'LPPTinfo' ## filename for 'this is Lisboa information'
        },
        'approaches': {
            '03': 'ils',
            '21': 'ils',
            '35': 'vor',
            '17': 'visual'
        },
        'transition_altitude': '4000'
    },
    'LPPR': {
        'fragments': {

            ###
            ### Fragments we need to specify
            ###
            'ident': 'LPPR', ## filename for 'Lisboa'
            'info': 'LPPRinfo' ## filename for 'this is Lisboa information'
        },
        'approaches': {
            '35': 'rnav',
            '17': 'ils'
        },
        'transition_altitude': '4000'
    },
    'LPFR': {
        'fragments': {

            ###
            ### Fragments we need to specify
            ###
            'ident': 'LPFR', ## filename for 'Lisboa'
            'info': 'LPFRinfo' ## filename for 'this is Lisboa information'
        },
        'approaches': {
            '10': 'vor',
            '28': 'ils'
        },
        'transition_altitude': '4000'
    },
    'LPMA': {
        'fragments': {

            ###
            ### Fragments we need to specify
            ###
            'ident': 'LPMA', ## filename for 'Lisboa'
            'info': 'LPMAinfo' ## filename for 'this is Lisboa information'
        },
        'approaches': {
            '05': 'vor',
            '23': 'vor'
        },
        'transition_altitude': '5000'
    }
}

def generateTemperatures(metar):
    return '[temperature]%d[dewpoint]%d' % (metar.temp._value, metar.dewpt._value)

def generatePressure(metar):
    return '[QNH]%d' % metar.press._value

def generateWinds(metar):
    wind_calm_template = '[wind calm]'
    wind_direction_sustained_template = '[wind]${wind_dir}[degrees]'
    wind_direction_variable_template = '[wind]${wind_dir}[variable betwen]${wind_dir_from}[and]${wind_dir_to}[degrees]'
    wind_speed_sustained_template = '${wind_speed}[knots]'
    wind_speed_gusting_template = '${wind_speed}[gusting to]${wind_gust}[knots]'
    dir_template = ''
    speed_template = ''
    template = ''
    if metar.wind_speed._value < 5.0:
        template = wind_calm_template
    else:
        dir_template = wind_direction_variable_template if metar.wind_dir_from._degrees and metar.wind_dir_to._degrees else wind_direction_sustained_template
        speed_template = wind_speed_gusting_template if metar.wind_gust else wind_speed_sustained_template

        template = dir_template + speed_template
    return Template(template).substitute(
        wind_dir='%03d' % metar.wind_dir_to._degrees,
        wind_dir_from='%03d' % metar.wind_dir_from._degrees,
        wind_dir_to='%03d' % metar.wind_dir_to._degrees,
        wind_speed='%d' % metar.wind_speed._value,
        wind_gust='%d' % metar.wind_gust._value)

def getTransisionLevel(ta, qnh):
    table = default['transition_level_table'][ta]

    table.sort()
    pos = bisect.bisect_right(table, (qnh,))
    return table[pos][1]

def generateATIS(metar, arrrwy, letter):
    metar = Metar.Metar(metar)

    # merge dicts
    airport = default
    dict_merge(airport, airports[metar.station_id])

    atis = airport['format']

    # station info
    atis = atis.replace('arrrwy', arrrwy)
    atis = atis.replace('letter', letter)

    # met report info
    atis = atis.replace('metar.time', metar.time.strftime("%H%M"))

    # set approach type
    atis = atis.replace('approach_type', airport['approaches'][arrrwy])

    # set transition transition
    atis = atis.replace('airport.ta', getTransisionLevel(airport['transition_altitude'], metar.press._value))

    # set winds
    atis = atis.replace('metar.winds', generateWinds(metar))

    # set temperatures
    atis = atis.replace('metar.temperatures', generateTemperatures(metar))

    # set pressure
    atis = atis.replace('metar.pressure', generatePressure(metar))

    # gnerates the atis text by populating the atis format string
    for key, value in airport['fragments'].items():
        atis = atis.replace(key, value)

    return atis

###
### By angstwad <https://gist.github.com/angstwad>
### https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
###
def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
