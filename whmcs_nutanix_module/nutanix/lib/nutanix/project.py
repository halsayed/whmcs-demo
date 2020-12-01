from .httpClient import CalmClient


def list(params):
    client = CalmClient(params)
    result = client.project_list()
    projects = []
    if len(result):
        for project in result:
            projects.append({project['metadata']['uuid']: project['spec']['name']})

    return projects
