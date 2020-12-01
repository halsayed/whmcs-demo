from .httpClient import CalmClient


def list(params):
    client = CalmClient(params)
    result = client.blueprint_list()
    blueprints = []
    for blueprint in result:
        blueprints.append({
            blueprint['metadata']['uuid']: blueprint['metadata']['name']
        })
    return blueprints


def launch(params):
    blueprint_name = str(params.get('configoption4'))
    password = str(params.get('password', ''))
    accountid = str(params.get('accountid', ''))
    userid = str(params.get('userid', ''))
    packageid = str(params.get('packageid', ''))
    blueprint_uuid = ''
    print([blueprint_uuid, password, accountid, userid, packageid])

    client = CalmClient(params)
    for blueprint in client.blueprint_list():
        if blueprint['metadata']['name'] == blueprint_name:
            blueprint_uuid = blueprint['metadata']['uuid']

    print([blueprint_uuid, password, accountid, userid, packageid])

    if '' not in [blueprint_uuid, password, accountid, userid, packageid]:
        blueprint = client.blueprint_get(blueprint_uuid)
        var_list = {'password': password, 'accountid': accountid, 'userid': userid, 'packageid': packageid}
        payload = {'spec': {}, 'api_version': '3.0', 'metadata': {}}
        payload['spec']['description'] = blueprint['spec']['description']
        payload['spec']['application_name'] = f'WHMCS-{userid}-{accountid}-{packageid}'
        payload['spec']['app_profile_reference'] = {'kind': 'app_profile'}
        payload['spec']['app_profile_reference']['uuid'] = blueprint['spec']['resources']['app_profile_list'][0]['uuid']
        payload['spec']['resources'] = blueprint['spec']['resources']

        # fill in the variable list
        vars = []
        for item in payload['spec']['resources']['app_profile_list'][0]['variable_list']:
            if item['name'] in var_list:
                item['value'] = var_list[item['name']]
            vars.append(item)

        payload['spec']['resources']['app_profile_list'][0]['variable_list'] = vars
        payload['metadata'] = blueprint['metadata']

        result = client.blueprint_launch(uuid=blueprint_uuid, payload=payload)
        if result:
            return 'success'
        else:
            return 'failure'
