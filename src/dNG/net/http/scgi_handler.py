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
#echo(pasHttpScgiVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error, no-name-in-module

from dNG.controller.http_scgi1_request import HttpScgi1Request
from dNG.data.binary import Binary
from dNG.net.server.handler import Handler
from dNG.runtime.io_exception import IOException

class ScgiHandler(Handler):
    """
"ScgiHandler" is an opened connection with an SCGI client.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: scgi
:since;      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    NETSTRING_SEPARATOR = Binary.bytes(":")
    """
netstring separator between length and string
    """

    # pylint: disable=invalid-name

    def _handle_headers(self, request):
        """
Receives and adds the request headers from the socket to the given request
instance.

:since:  v0.1.00
        """

        headers_data = self._get_netstring()
        items = headers_data.split("\x00")

        if (len(items) % 2 != 0): raise IOException("SCGI headers received are invalid")

        for i in range(0, len(items), 2):
            if (items[i][:5] == "HTTP_"):
                header_name = items[i][5:].replace("_", "-").upper()
                if (header_name != "CONTENT-LENGTH"): request.set_header(header_name, items[i + 1])
            else: request.set_scgi_header(items[i].upper(), items[i + 1])
        #
    #

    def _get_netstring(self):
        """
Receives the netstring from the socket.

:return: (str) Size of the netstring following
:since:  v0.1.00
        """

        netstring_size = self._get_netstring_size()
        return Binary.str(self.get_data(1 + netstring_size, True)[:-2])
    #

    def _get_netstring_size(self):
        """
Receives the netstring size from the socket.

:return: (int) Size of the netstring following
:since:  v0.1.00
        """

        data = Binary.BYTES_TYPE()
        netstring_char = None

        while (netstring_char != ScgiHandler.NETSTRING_SEPARATOR):
            netstring_char = self.get_data(1)
            if (netstring_char != ScgiHandler.NETSTRING_SEPARATOR): data += netstring_char
        #

        return int(data)
    #

    def read(self, n = 0):
        """
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.00
        """

        return self.get_data(n)
    #

    def _thread_run(self):
        """
Active SCGI connection

:since: v0.1.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._thread_run()- (#echo(__LINE__)#)", self, context = "pas_http_scgi")

        request = HttpScgi1Request()
        self._handle_headers(request)

        if (request.get_scgi_header("SCGI") != "1"
            or request.get_scgi_header("CONTENT_LENGTH") is None
           ): raise IOException("SCGI headers received are invalid")

        request.set_scgi_handler(self)
        request.handle_scgi_request()
    #
#
