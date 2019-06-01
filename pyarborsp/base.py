"""
Setting up the base API sessions to ArborSP
"""

import requests
import urllib3


class ArborAPI:
    """Fetches data and controls DDoS attacks from ArborSP"""

    def __init__(self, url, token, verify_ssl=True, https_warning=True):
        """
        :param url: URL of the ArborSP service
        :type url: ``str``
        :param token: API Token
        :type token: ``str``
        :param verify_ssl: Verify SSL certificate from the requests package
        :type verify_ssl: ``bool``
        :param https_warning: Prompt with HTTPS warnings from the requests package
        :type https_warning: ``bool``
        """
        self.url = url
        self.token = token
        self.https_warning = https_warning
        self.verify_ssl = verify_ssl
        self.headers = {
            "X-Arbux-APIToken": self.token,
        }

        if self.https_warning is False:
            from urllib3.exceptions import InsecureRequestWarning
            urllib3.disable_warnings(InsecureRequestWarning)

    def _get(self, url):
        return requests.get(url, headers=self.headers, verify=self.verify_ssl).json()

    def _post(self, url, payload):
        return requests.post(url, headers=self.headers, json=payload, verify=self.verify_ssl)

    def _patch(self, url, payload):
        return requests.patch(url, headers=self.headers, json=payload, verify=self.verify_ssl)

    def _change_mitigation_state(self, mitigation_id, status=bool()):
        data = {
            "data": {
                "attributes": {
                    "ongoing": status
                }
            }
        }
        url = self._get(self.url)['links']['mitigation']
        url += "/{}".format(mitigation_id)
        return self._patch(url=url, payload=data).json()

    def meta(self):
        """
        Fetch meta data from ArborSP

        :returns: ``dict``

        """
        return self._get(self.url)['meta']

    def endpoints(self):
        """
        Fetch available API endpoints

        :returns: ``dict``

        """
        return self._get(self.url)

    def endpoint(self, endpoint):
        """
        Fetch data from an API endpoint

        :param endpoint: URL of API endpoint
        :type endpoint: ``str``
        :returns: ``dict``
        :raises: KeyError

        """
        try:
            url = self._get(self.url)['links'][endpoint]
            return self._get(url)
        except KeyError:
            return {"Error": "Endpoint {} does not exit".format(endpoint)}

    def ongoing(self, mitigation_id=None, mitigation_type="tms"):
        """
        Fetch ongoing blackhole or tms mitigations

        :param mitigation_id: tms-1234 or blackhole-1234
        :type mitigation_id: ``str`` or ``None``
        :param mitigation_type: tms or blackhole, default: tms
        :type mitigation_type: ``str``
        :returns: ``dict``

        """
        if mitigation_id:
            url = str(self._get(self.url)['links']['mitigation'])
            url += "/{}".format(mitigation_id)
            return self._get(url)
        url = str(self._get(self.url)['links']['mitigation'])
        data = self._get(url)['data']
        ongoing = list()

        for item in data:
            if item['attributes']['ongoing']:
                if item['attributes']['subtype'] == mitigation_type:
                    ongoing.append(item)
        return ongoing

    def start(self, mitigation_id):
        """
        Start an existing mitigation

        :param mitigation_id: tms-1234 or blackhole-1234
        :returns: ``dict``

        """
        return self._change_mitigation_state(mitigation_id, status=True)

    def stop(self, mitigation_id):
        """
        Stop an existing mitigation

        :param mitigation_id: tms-1234 or blackhole-1234
        :returns: ``dict``

        """
        return self._change_mitigation_state(mitigation_id, status=False)
