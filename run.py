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

from eve import Eve
from flask import request
import os

app = Eve()

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    host = '0.0.0.0'
    debug = False
else:
    port = 5000
    host = '0.0.0.0'
    debug = True

@app.route('/generate/<string:airport>')
def generate(airport):

    metar = request.args['metar']
    arrrwy = request.args['arrrwy']
    letter = request.args['letter']

    return ''
    return '[' + airport + 'info]' + letter + '[runway in use]' + arrrwy + '[endof][' + airport + '][atis]' + letter

if __name__ == '__main__':
	app.run(host=host, port=port, debug=debug)
