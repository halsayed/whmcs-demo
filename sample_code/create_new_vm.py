import os
import base64
import requests
import time

# disable ssl warnings
import urllib3
urllib3.disable_warnings()

# API configuration and parameters ...
pc_address = '127.0.0.1'
username = 'admin'
password = os.environ.get('PASSWORD')  # change the password to a suitable value
authorization = base64.b64encode(f'{username}:{password}'.encode()).decode()
url = f'https://{pc_address}:9440/api/nutanix/v3'
kwargs = {
    'verify': False,
    'headers': {'Authorization': f'Basic {authorization}'}
}

# ==========================================================================================
# Define the new VM parameters
# ==========================================================================================
vm_name = 'test_vm_api'
sockets = 2
vcpu_per_socket = 1
memory = 4096
network_uuid = 'fa8b4999-6b07-4893-a435-2e1b578133dc'
os_image_uuid = 'f4867063-fd5f-491f-96db-834b531dd431'
os_image_size = 10240   # in MiB
cluster_uuid = '0005a07a-80f6-43b4-6f8e-ac1f6b3bba76'
cloud_init = "#cloud-config\nssh_pwauth: True\nchpasswd:\n  list: |\n     ubuntu:nutanix/4u\n  expire: False\nusers:\n  - name: ubuntu\n    sudo: ['ALL=(ALL) NOPASSWD:ALL']\n    shell: /bin/bash"

# ==========================================================================================
# Construct Post payload and perform API call
# ==========================================================================================
payload = {
    'spec': {
        'name': vm_name,
        'resources': {
            'memory_size_mib': memory,
            'num_sockets': sockets,
            'num_vcpus_per_socket': vcpu_per_socket,
            'disk_list': [
                {
                    'device_properties': {
                        'device_type': 'DISK',
                        'disk_address': {
                            'device_index': 0,
                            'adapter_type': 'SCSI'
                        }
                    },
                    'data_source_reference': {
                        'kind': 'image',
                        'uuid': os_image_uuid
                    },
                    'disk_size_mib': os_image_size
                }
            ],
            'guest_customization': {
                'cloud_init': {
                    'user_data': base64.b64encode(cloud_init.encode()).decode()
                }
            },
            'nic_list': [
                {
                    'nic_type': 'NORMAL_NIC',
                    'vlan_mode': 'ACCESS',
                    'subnet_reference': {
                        'kind': 'subnet',
                        'uuid': network_uuid
                    },
                    'is_connected': True
                }
            ]
        },
        'cluster_reference': {
            'kind': 'cluster',
            'uuid': cluster_uuid
        }
    },
    'api_version': '3.1.0',
    'metadata': {
        'kind': 'vm'
    }
}

# perform post api
resp = requests.post(f'{url}/vms', json=payload, **kwargs)
if resp.status_code == 202:
    task_uuid = resp.json()["status"]["execution_context"]["task_uuid"]
    vm_uuid = resp.json()['metadata']['uuid']
    print(f'VM request submitted successfully, task_uuid: {task_uuid}, vm_uuid: {vm_uuid}')
else:
    print(f'ERROR - VM creation failed, status code: {resp.status_code}, message: {resp.content}')
    exit(1)


# ==========================================================================================
# Check status of VM creation task
# ==========================================================================================
status = 'RUNNING'
count = 1
while status == 'RUNNING':
    resp = requests.get(f'{url}/tasks/{task_uuid}', **kwargs)
    if resp.status_code == 200:
        status = resp.json()['status']
        print(f'check {count} - Task status: {status}')
        count += 1
        time.sleep(1)
    else:
        print(f'ERROR - task status check failed, status code: {resp.status_code}, message: {resp.content}')
        exit(1)

print(f'Final task status: {status}')


# ==========================================================================================
# Power on VM by changing the state
# ==========================================================================================
print('VM is ready, powering on VM')
resp = requests.get(f'{url}/vms/{vm_uuid}', **kwargs)
payload = resp.json()
del(payload['status'])
payload['spec']['resources']['power_state'] = 'ON'
resp = requests.put(f'{url}/vms/{vm_uuid}', json=payload, **kwargs)
print(f'Powering status code: {resp.status_code}')


