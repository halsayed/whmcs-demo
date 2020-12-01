
def on(params):
    print('power on')
    print(params)
    return {'status': 'on'}


def off(params):
    print('power off')
    print(params)
    return {'status': 'off'}
