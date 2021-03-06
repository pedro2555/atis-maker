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

from eve import Eve
from flask import request
import os
import atis

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

@app.route('/generate')
def generate():
    return atis.generateATIS(request.args['metar'],
                             request.args['arrrwy'],
                             request.args['letter'])

if __name__ == '__main__':
	app.run(host=host, port=port, debug=debug)
