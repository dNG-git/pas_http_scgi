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

import re
import socket

from dNG.data.settings import Settings
from dNG.data.logging.log_line import LogLine
from dNG.net.server.dispatcher import Dispatcher

from .scgi_handler import ScgiHandler

class ScgiDispatcher(Dispatcher):
    """
"ScgiDispatcher" provides a SCGI server.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: scgi
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    # pylint: disable=unused-argument

    def __init__(self):
    #
        """
Constructor __init__(ScgiDispatcher)

:since: v0.1.00
        """

        listener_address = Settings.get("pas_http_scgi_listener_address")
        listener_mode = Settings.get("pas_http_scgi_listener_mode")

        if (listener_mode == "ipv6"): listener_mode = socket.AF_INET6
        elif (listener_mode == "ipv4"): listener_mode = socket.AF_INET

        try:
            if (listener_mode is None or listener_mode == "unixsocket"):
                listener_mode = socket.AF_UNIX
                if (listener_address is None): listener_address = "/tmp/dNG.pas.http.SCGI.socket"
            elif (listener_address is None): listener_address = "localhost:2303"
        except AttributeError:
            listener_mode = socket.AF_INET
            listener_address = "localhost:2303"
        #

        listener_data = set()

        if (listener_mode in ( socket.AF_INET, socket.AF_INET6 )):
            re_result = re.search("^(.+):(\\d+)$", listener_address)

            if (re_result is None):
                listener_data.add(listener_address)
                listener_data.add(None)
            else:
                listener_data.add(re_result.group(1))
                listener_data.add(int(re_result.group(2)))
            #
        else: listener_data.add(listener_address)

        listener_socket = Dispatcher.prepare_socket(listener_mode, *listener_data)
        LogLine.info("pas.http.scgi server starts at '{0}'", listener_address, context = "pas_http_scgi")

        listener_max_actives = int(Settings.get("pas_http_scgi_listener_actives_max", 100))
        Dispatcher.__init__(self, listener_socket, ScgiHandler, listener_max_actives)
    #
#
