"""C-CEX REST API backend.

Documentation available here:
    https://c-cex.com/?id=api
"""
# Import Built-ins
import logging
import hashlib
import hmac

# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class CCEXREST(RESTAPI):
    """C-CEX REST API class."""

    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        """Initialize the class instance."""
        addr = 'https://c-cex.com/t' if not addr else addr

        super(CCEXREST, self).__init__(addr=addr, version=version, key=key,
                                       secret=secret, timeout=timeout,
                                       config=config)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Sign the request."""
        req_kwargs = super(CCEXREST, self).sign_request_kwargs(endpoint,
                                                               **kwargs)

        # Prepare Payload arguments
        nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        params['apikey'] = self.key
        params['nonce'] = nonce
        url = self.addr + '/' + endpoint

        # generate signature
        sig = hmac.new(self.secret.encode('utf-8'), url.encode('utf-8'),
                       hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['params'] = params
        req_kwargs['headers'] = {'apisign': sig}
        req_kwargs['url'] = url

        return req_kwargs
