from .httpClient import CalmClient


def list(params):
    client = CalmClient(params)
    result = client.marketplace_list()
    items = []
    for item in result:
        items.append({
            'name': item['metadata']['name'],
            'uuid': item['metadata']['uuid'],
            # 'description': item['status']['description'],
        })
    return items
