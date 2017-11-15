class ArborAPI(object):
    """Fetches data and controls DDoS attacks from ArborSP

    Args:
      **arbor_auth** (``dict``)
        **url** (``str``)
          Example: https://arborsp.example.com
        **token** (``str``)
          Example: ASDFasdfASDFasdfASDFasd
        **verify_ssl** (``bool``)
          Default: True
        **https_warning** (``bool``)
          Default: True

    Example:
      ``arbor_auth = {
            "url": "https://arbor.example.com",
            "token": "ASDFasdfASDFasdfASDF",
        }``

    """

    def __init__(self, arbor_args):
        self.token = arbor_args['token']
        self.url = arbor_args['url']
        try:
            self.https_warning = arbor_args['https_warning']
        except:
            self.https_warning = True
        try:
            self.verify_ssl = arbor_args['verify_ssl']
        except:
            self.verify_ssl = True
        self.headers = {
            "X-Arbux-APIToken": self.token,
            "Content-Type": 'application/vnd.api+json',
        }

        if self.https_warning is False:
            import requests
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


    def _get(self, url):
        import requests

        return requests.get(
            url,
            headers=self.headers,
            verify=self.verify_ssl
        ).json()

    def _post(self, url, payload):
        import requests

        return requests.post(
            url,
            headers=self.headers,
            json=payload,
            verify=self.verify_ssl
        )

    def _patch(self, url, payload):
        import requests

        return requests.patch(
            url,
            headers=self.headers,
            json=payload,
            verify=self.verify_ssl
        )

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
        response = self._patch(url=url, payload=data)

        return response.json()

    def get_meta(self):
        """Fetch meta data from ArborSP
        :returns: ``dict``

        """
        return self._get(self.url)['meta']

    def get_endpoints(self):
        """Fetch available API endpoints
        :returns: ``dict``

        """
        return self._get(self.url)['links']

    def endpoint(self, endpoint):
        """Fetch data from an API endpoint
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

    def ongoing_mitigations(self, mitigation_id=None):
        """Fetch ongoing mitigations
        :param migitation_id: tms-1234
        :type mitigation_id: ``str`` or ``None``
        :returns: ``dict``

        """
        if mitigation_id:
            url = str(self._get(self.url)['links']['mitigation'])
            url += "/{}".format(mitigation_id)

            return self._get(url)
        else:
            url = str(self._get(self.url)['links']['mitigation'])
            data = self._get(url)['data']
            ongoing = list()

            for item in data:
                if item['attributes']['ongoing']:
                    if item['attributes']['subtype'] == 'tms':
                        ongoing.append(item)

            return ongoing

    def ongoing_rtbhs(self, mitigation_id=None):
        """Fetch ongoing blackhole mitigations 
        :param migitation_id: blackhole-1234
        :type mitigation_id: ``str`` or ``None``
        :returns: ``dict``

        """
        if mitigation_id:
            return self.ongoing_mitigations(mitigation_id)
        else:
            url = str(self._get(self.url)['links']['mitigation'])
            data = self._get(url)['data']
            ongoing = list()

            for item in data:
                if item['attributes']['ongoing']:
                    if item['attributes']['subtype'] == 'blackhole':
                        ongoing.append(item)

            return ongoing

    def start_mitigation(self, mitigation_id):
        """Start an existing mitigation
        :param mitigation_id: tms-1234 or blackhole-1234
        :returns: ``dict``

        """
        return self._change_mitigation_state(mitigation_id, status=True)

    def stop_mitigation(self, mitigation_id):
        """Stop an existing mitigation
        :param mitigation_id: tms-1234 or blackhole-1234
        :returns: ``dict``

        """
        return self._change_mitigation_state(mitigation_id, status=False)
