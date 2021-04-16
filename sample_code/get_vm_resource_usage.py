import os
import base64
import requests
from time import time
from datetime import datetime
from pprint import pprint

# disable ssl warnings
import urllib3
urllib3.disable_warnings()

# API configuration and parameters ...
pc_address = '10.38.7.9'
username = 'admin'
password = os.environ.get('PASSWORD', 'nx2Tech911!')  # change the password to a suitable value
authorization = base64.b64encode(f'{username}:{password}'.encode()).decode()
url = f'https://{pc_address}:9440/api/nutanix/v3'
kwargs = {
    'verify': False,
    'headers': {'Authorization': f'Basic {authorization}'}
}


# ==========================================================================================
# Define the new VM parameters
# ==========================================================================================
vm_uuid = 'c700239e-facf-44be-b7ed-34b277f784b2'
print(f'===========================================\nGet VM average usage for last 5min\n===========================================')

payload = {
    'entity_type': 'mh_vm',
    'entity_ids': [vm_uuid],
    'grouping_attribute': 'vm',
    'group_member_attributes': [
        {'attribute': 'hypervisor_cpu_usage_ppm', 'operation': 'AVG'},
        {'attribute': 'memory_usage_ppm', 'operation': 'AVG'},
        {'attribute': 'hypervisor_num_received_bytes'},
        {'attribute': 'hypervisor_num_transmitted_bytes'}
    ],
    'interval_end_ms': int(time()*1000),
    'interval_start_ms': int((time()-300)*1000),
    'downsampling_interval': 300,
    'query_name': 'prism:CPStatsModel',
    'availability_zone_scope': 'GLOBAL',
    'filter_criteria': '(platform_type!=aws,platform_type==[no_val])'
}

resp = requests.post(f'{url}/groups', json=payload, **kwargs)
result = resp.json()
# pprint(result['group_results'][0]['entity_results'][0]['data'])
for resource in result['group_results'][0]['entity_results'][0]['data']:
    resource_name = resource['name']
    resource_value = resource['values'][0]['values'][0]
    timestamp = int(resource['values'][0]['time'])/1000000
    if not resource_name[:1] == '_':
        print(f'{datetime.fromtimestamp(time())} - {resource_name}: {resource_value}')

