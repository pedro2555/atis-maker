#!/usr/bin/env python
"""
<one line to give the program's name and a brief idea of what it does.>
Copyright (C) <year>  <name of author>

This file is part of Foobar.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
import collections
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
        'ils': 'expect ILS', ## filename for 'expect ILS approach'
        'rnav': '', ## filename for 'expect RNAV approach'
        'vor': 'expect VOR', ## filename for 'expect VOR DME approach'
        'ndb': '', ## filename for 'expect NDB approach'
        'visual': '', ## filename for 'expect visual approach'

        'runway_in_use': 'runway in use', ## filename for 'runway in use'

        'transition_level': 'transition level', ## filename for 'transition level'

        'end': 'endof', ## filename for 'end of'
        'atis': 'atis' ## filename for 'atis'
    },
    'format': '[info]lettermetar.time[approach_type][runway_in_use]arrrwy[transition_level][end][ident]letter'
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
        }
    }
}

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
    atis = atis.replace('metar.time', str(metar.time.hour) + str(metar.time.hour))

    # set approach type
    atis = atis.replace('approach_type', airport['approaches'][arrrwy])

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
