# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;scgi

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error

from .abstract_http_cgi_stream_response import AbstractHttpCgiStreamResponse

class HttpScgi1StreamResponse(AbstractHttpCgiStreamResponse):
    """
This stream response instance will write all data to the underlying SCGI 1.0
connection handler.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: scgi
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def __init__(self, scgi_handler):
        """
Constructor __init__(HttpScgi1StreamResponse)

:param scgi_handler: SCGI handler for this response.

:since: v0.1.00
        """

        AbstractHttpCgiStreamResponse.__init__(self)

        self._handler = scgi_handler
        """
SCGI connection handler
        """
    #

    def send_headers(self):
        """
Sends the prepared response headers.

:since: v0.1.00
        """

        # pylint: disable=attribute-defined-outside-init

        http_status_line = "200 OK"

        headers = [ ]
        headers_indexed = dict([( value, key ) for ( key, value ) in self.headers_indexed.items()])
        filtered_headers = self._filter_headers()

        for header_name in filtered_headers:
            if (type(header_name) is int):
                header_value = str(filtered_headers[header_name])
                header_name = headers_indexed[header_name]

                if (header_name == "HTTP"): http_status_line = header_value[9:]
                else: headers.append(( header_name, header_value ))
            elif (type(filtered_headers[header_name]) is list):
                for header_list_value in filtered_headers[header_name]:
                    header_list_value = str(header_list_value)
                    headers.append(( header_name, header_list_value ))
                #
            else:
                header_value = str(filtered_headers[header_name])
                headers.append(( header_name, header_value ))
            #
        #

        data = "Status: {0}\r\n".format(http_status_line)
        for header in headers: data += "{0}: {1}\r\n".format(header[0], header[1])
        data += "\r\n"

        self.headers_sent = True
        self._write(data)
    #

    def _write(self, data):
        """
Writes the given data.

:param data: Data to be send

:since: v0.1.00
        """

        # pylint: disable=attribute-defined-outside-init

        if (not self.headers_sent): self.send_headers()
        if (not self._handler.write_data(data)): self.active = False
    #
#
