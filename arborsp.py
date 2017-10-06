class ArborAPI(object):

    # 1. Create Arbor Auth Dictionary
    #
    # arbor_auth = {
    #    "url": "https://arborsp.example.com",
    #    "token": "ASDFasdfASDFasdfASDFasdf",
    #    "verify_ssl": False,
    # }
    #
    # 2. Call API
    #
    # arbor = ArborAPI(arbor_auth)
    # arbor.ongoing_mitigations()

    def __init__(self, arbor_args):
        self.token = arbor_args['token']
        self.url = arbor_args['url']
        try:
            self.verify_ssl = arbor_args['verify_ssl']
        except:
            self.verify_ssl = True

    def _get(self, url):
        import requests

        return requests.get(
            url,
            headers={"X-Arbux-APIToken": self.token},
            verify=self.verify_ssl
        ).json()

    def _post(self, url, payload):
        import requests

        return requests.post(
            url,
            headers={"X-Arbux-APIToken": self.token},
            json=payload,
            verify=self.verify_ssl
        )

    def _patch(self, url, payload):
        import requests

        return requests.patch(
            url,
            headers={"X-Arbux-APIToken": self.token},
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
        return self._get(self.url)['meta']

    def get_endpoints(self):
        return self._get(self.url)['links']

    def endpoint(self, endpoint):
        try:
            url = self._get(self.url)['links'][endpoint]
            return self._get(url)
        except KeyError:
            return {"Error": "Endpoint {} does not exit".format(endpoint)}

    def ongoing_mitigations(self, mitigation_id=None):
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
        return self._change_mitigation_state(mitigation_id, status=True)

    def stop_mitigation(self, mitigation_id):
        return self._change_mitigation_state(mitigation_id, status=False)

    def create_rtbh(self, region, pfx, duration=None, ipver='ipv4'):
        pass
