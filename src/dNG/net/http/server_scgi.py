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

from dNG.runtime.exception_log_trap import ExceptionLogTrap
from dNG.net.http.abstract_server import AbstractServer

from .scgi_dispatcher import ScgiDispatcher

class ServerScgi(AbstractServer):
    """
"ServerScgi" takes requests from SCGI aware clients.

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
Constructor __init__(ServerScgi)

:since: v0.1.00
        """

        AbstractServer.__init__(self)

        self.server = None
        """
WSGI server
        """
    #

    def _configure(self):
    #
        """
Configures the server

:since: v0.1.00
        """

        self.server = ScgiDispatcher()

        AbstractServer._configure(self)
    #

    def run(self):
        """
Runs the server

:since: v0.1.00
        """

        with ExceptionLogTrap("pas_http_scgi"): self.server.run()
    #

    def stop(self, params = None, last_return = None):
        """
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
        """

        if (self.server is not None): self.server.stop()
        return AbstractServer.stop(self, params, last_return)
    #
#
