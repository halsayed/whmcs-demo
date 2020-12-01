import requests
import os
from urllib.parse import urljoin
from .logger import log
import urllib3


class CalmClient(requests.Session):

    def __init__(self, params, verify_ssl=False):
        self.base_url = ''
        super().__init__()
        self.verify = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings()

        prism_ip = os.environ.get('CALM_DSL_PC_IP') or params.get('serverip')
        prism_port = os.environ.get('CALM_DSL_PC_PORT') or '9440'
        username = os.environ.get('CALM_DSL_PC_USERNAME') or params.get('serverusername')
        password = os.environ.get('CALM_DSL_PC_PASSWORD') or params.get('serverpassword')
        self.base_url = f'https://{prism_ip}:{prism_port}/api/nutanix/v3/'
        self.auth = (username, password)

    def application_list(self, state=None):
        # TODO: add pagination if more than 250 apps
        # TODO: handle application state filter
        payload = {'kind': 'app', 'length': 250}
        url = urljoin(self.base_url, 'apps/list')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()['entities']
        else:
            log.error(f'List application API call failed, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def project_list(self):
        payload = {'kind': 'project', 'length': 100}
        url = urljoin(self.base_url, 'projects/list')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()['entities']
        else:
            log.error(f'List project API call failed, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def marketplace_list(self):
        payload = {'kind': 'marketplace_item', 'filter': 'app_state==PUBLISHED', 'length': 100}
        url = urljoin(self.base_url, 'calm_marketplace_items/list')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()['entities']
        else:
            log.error(f'List of marketplace items API failed, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def blueprint_list(self):
        payload = {'kind': 'blueprint', 'filter': 'state==ACTIVE', 'length': 100}
        url = urljoin(self.base_url, 'blueprints/list')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()['entities']
        else:
            log.error(f'Blueprint list API call failed, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def blueprint_get(self, uuid):
        url = urljoin(self.base_url,f'blueprints/{uuid}')
        resp = self.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            log.error(f'Blueprint get API failed, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def blueprint_launch(self, uuid, payload):
        url = urljoin(self.base_url, f'blueprints/{uuid}/launch')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()
        else:
            log.error(f'Error in launch blueprint api call, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def app_action(self, uuid, name, args=[]):
        payload = {'name': name, 'args': args}
        url = urljoin(self.base_url, f'apps/{uuid}/actions/run')
        resp = self.post(url, json=payload)
        if resp.status_code == 200:
            return resp.json()
        else:
            log.error(f'Error in action: {name} run, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

    def app_delete(self, uuid):
        url = urljoin(self.base_url, f'apps/{uuid}')
        resp = self.delete(url)
        if resp.status_code == 200:
            return 'success'
        else:
            log.error(f'Error in delete application: {uuid}, status code: {resp.status_code}')
            log.error(f'Msg: {resp.content}')

