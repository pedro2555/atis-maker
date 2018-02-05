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

from string import Template

class AtisTemplate(Template):
    delimiter='$atis'

class MetarTemplate(Template):
    delimiter='$metar'

template = Template('This is $metar{station} information $atis{letter} time $metar{time}')
template.delimiter='$metar'
print(template)
template = Template(template.safe_substitute(station='LPPT',time='0530'))
print(template.safe_substitute(letter='A'))
