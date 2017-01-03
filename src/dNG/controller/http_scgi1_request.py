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

from dNG.data.settings import Settings
from dNG.runtime.exception_log_trap import ExceptionLogTrap

from .abstract_http_cgi_request import AbstractHttpCgiRequest
from .http_scgi1_stream_response import HttpScgi1StreamResponse

class HttpScgi1Request(AbstractHttpCgiRequest):
    """
"HttpScgi1Request" handles a SCGI client request.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: scgi
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def __init__(self):
        """
Constructor __init__(HttpScgi1Request)

:since: v0.1.00
        """

        AbstractHttpCgiRequest.__init__(self)

        self._handler = None
        """
SCGI connection handler
        """
        self.scgi_headers = { }
        """
SCGI request headers
        """
        self._stream_response = None
        """
The SCGI stream response instance
        """
    #

    def get_scgi_header(self, name):
        """
Returns the SCGI request header if defined.

:param name: Header name

:return: (str) Header value if set; None otherwise
:since:  v0.1.00
        """

        name = name.upper()
        return self.scgi_headers.get(name)
    #

    def handle_scgi_request(self):
        """
Handles a SCGI compliant resource request.

:since: v0.1.00
        """

        # pylint: disable=attribute-defined-outside-init, broad-except, no-member, protected-access

        self.server_host = Settings.get("pas_http_server_forced_hostname")
        self.server_port = Settings.get("pas_http_server_forced_port")

        self._handle_host_definition_headers(self.headers, [ "HOST" ])

        if (self.server_host is None):
            self.server_host = Settings.get("pas_http_server_preferred_hostname")
            if (self.server_port is None): self.server_port = Settings.get("pas_http_server_preferred_port")
        #

        self._handle_cgi_headers(self.scgi_headers)

        headers = self.headers.copy()
        headers.update(self.scgi_headers)

        self._handle_remote_address_headers(headers)
        self._rewrite_client_ipv4_in_ipv6_address()

        self._stream_response = HttpScgi1StreamResponse(self._handler)

        try:
            re_object = HttpScgi1Request.RE_SERVER_PROTOCOL_VERSION.match(self.scgi_headers.get("SERVER_PROTOCOL", ""))
            if (re_object is not None): self._stream_response.set_http_version(float(re_object.group(1)))

            self.body_fp = self._handler

            scheme_header = Settings.get("pas_http_server_scheme_header", "")
            self.server_scheme = (None if (scheme_header == "") else self.headers.get(scheme_header.upper().replace("-", "_")))

            if (self.script_path_name is None): self.script_path_name = ""

            if (not (self.get_header("Upgrade") is not None
                     and self._handle_upgrade(self.virtual_path_name, self.http_wsgi_stream_response)
                    )
               ): self.execute()
        except Exception as handled_exception:
            if (self.log_handler is not None): self.log_handler.error(handled_exception, "pas_http_scgi")

            # Died before output
            if (not self._stream_response.are_headers_sent()):
                self._stream_response.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
                self._stream_response.send_data("Internal Server Error")
            #
        #

        with ExceptionLogTrap("pas_http_scgi"):
            for data in self._stream_response: self._stream_response._write(data)
        #
    #

    def _init_stream_response(self):
        """
Initializes the matching stream response instance.

:return: (object) Stream response object
:since:  v0.1.00
        """

        return self._stream_response
    #

    def set_scgi_handler(self, handler):
        """
Sets the SCGI handler for this request.

:param handler: SCGI handler for this request.

:since: v0.1.00
        """

        self._handler = handler
    #

    def set_scgi_header(self, name, value):
        """
Sets the SCGI header with the given name and value.

:param name: Header name
:param value: Header value

:since: v0.1.00
        """

        name = name.upper()
        self.scgi_headers[name] = value
    #
#
