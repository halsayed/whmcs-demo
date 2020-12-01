from .httpClient import CalmClient


def list(params):
    client = CalmClient(params)
    result = client.application_list()
    apps = []
    for app in result:
        apps.append({
            'name': app['metadata']['name'],
            'uuid': app['metadata']['uuid'],
            'project': app['metadata']['project_reference']['name'],
            'status': app['status']['state'],
        })
    return apps


def run_action(params, action_name, args):
    userid = params.get('userid')
    accountid = params.get('accountid')
    packageid = params.get('packageid')
    app_name = f'WHMCS-{userid}-{accountid}-{packageid}'
    app_uuid = ''
    client = CalmClient(params)
    result = client.application_list()
    for app in result:
        if app['metadata']['name'] == app_name:
            app_uuid = app['metadata']['uuid']

    if app_uuid:
        if action_name == 'action_delete':
            result = client.app_delete(app_uuid)
        else:
            result = client.app_action(app_uuid, action_name, args)
        if result:
            return 'success'
        else:
            return 'failre'


def stop(params):
    action_name = 'action_stop'
    args = []
    return run_action(params, action_name, args)


def start(params):
    action_name = 'action_start'
    args = []
    return run_action(params, action_name, args)


def delete(params):
    action_name = 'action_delete'
    args = []
    return run_action(params, action_name, args)


def update_password(params):
    action_name = 'update_password'
    password = params.get('password')
    args = [{'name': 'password', 'value':  password}]
    return run_action(params, action_name, args)


