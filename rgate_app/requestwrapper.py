import requests
from requests.adapters import HTTPAdapter


class requestsWrapper:
    """Custom request warpper"""
    def __init__(self):
        """
        """
        self.session = requests.Session()

    def safe_request(self, url, payload, method, **kwargs):
        """
        This calls the given url and payload in rest way
        kwargs can be passed auth, headers, timeout etc..
        """
        # Initial declarations
        resp = ''
        payload = payload or {}
        MAX_TRY = kwargs.pop('retry_limit', 1)
        self.session.mount(url, HTTPAdapter(max_retries=MAX_TRY))
        caller_mod = getattr(self.session, method.lower())

        try:
            resp = caller_mod(url, data=payload, **kwargs)
        except Exception as e:
            print(e)
            return None, None
        if resp.status_code:
            status_code = resp.status_code
            content_type = resp.headers.get('content-type')
            if 'json' in content_type:
                return resp.json(), status_code
            elif 'text' in content_type:
                return resp.text, status_code
            else:
                return resp, status_code
        else:
            print(f'Unable to {method} to {url} upto retry limit {MAX_TRY}')
            return None, None
