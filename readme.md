pyArborSP
---

This library utilizes the REST API interface from Arbor Networks. It's still in early development, so features are limited. Currently, the library can be utilized to display endpoints, and view ongoing mitigations/blackholes.

# Example Usage
```
$ cat test.py
#!/usr/local/bin/python3

from arborsp import ArborAPI
import json

if __name__ == "__main__":
    arbor_args = {
        "url": "https://arborsp.example.com/api/sp/",
        "token": "ASDFasdfASDFasdfASDFasdfASDFasdf",
        "verify_ssl": True,
    }
    a = ArborAPI(arbor_args)
    print(json.dumps(a.get_endpoints(), indent=2))


$ ./test.py
{
  "bgp_trap": "https://arborsp.example.com/api/sp/v2/bgp_traps/",
  "mitigation_template": "https://arborsp.example.com/api/sp/v2/mitigation_templates/",
  "tms_port": "https://arborsp.example.com/api/sp/v2/tms_ports/",
  "learning_mitigation": "https://arborsp.example.com/api/sp/v2/learning_mitigations/",
  "tms_filter_list": "https://arborsp.example.com/api/sp/v2/tms_filter_lists/",
  "self": "https://arborsp.example.com/api/sp/v2/",
  "insight": "https://arborsp.example.com/api/sp/v2/insight/",
  "managed_object": "https://arborsp.example.com/api/sp/v2/managed_objects/",
  "alert": "https://arborsp.example.com/api/sp/v2/alerts/",
  "application": "https://arborsp.example.com/api/sp/v2/applications/",
  "notification_group": "https://arborsp.example.com/api/sp/v2/notification_groups/",
  "mitigation": "https://arborsp.example.com/api/sp/v2/mitigations/",
  "tms_group": "https://arborsp.example.com/api/sp/v2/tms_groups/",
  "fingerprint": "https://arborsp.example.com/api/sp/v2/fingerprints/",
  "device": "https://arborsp.example.com/api/sp/v2/devices/",
  "router": "https://arborsp.example.com/api/sp/v2/routers/",
  "shared_host_detection_settings": "https://arborsp.example.com/api/sp/v2/shared_host_detection_settings/",
  "configuration": "https://arborsp.example.com/api/sp/v2/config/",
  "global_detection_settings": "https://arborsp.example.com/api/sp/v2/global_detection_settings"
}
```
