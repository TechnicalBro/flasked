"""
Application-wide exceptions module
"""

from flask_jsonrpc.exceptions import Error


class {{cookiecutter.app_name}}Error(Error):
    """
    Raised when the called subsystem or service layer experiences a server-side error

    :Example:

    ::

        [JSON-RPC RESPONSE - TESTING CONDITIONS]
            {
                'jsonrpc': '2.0',
                'error': {
                    'code': 500,
                    'data': None,
                    'message': 'Failed',
                    'name': 'PortalError',
                },
                'id': 0
            }

        [JSON-RPC RESPONSE - NORMAL CONDITIONS]
            {
                'jsonrpc': '2.0',
                'error': {
                    'code': 500,
                    'message': 'Failed',
                },
                'id': 0
            }

    """
    status = 500