import sys
import base64
import json
from nutanix import *


def main():
    # TODO: error handling for cli args
    command = sys.argv[1]
    params_b64 = sys.argv[2]

    # TODO: error handling for parameters decoding
    json_params = base64.b64decode(params_b64).decode()
    params = json.loads(json_params)

    if sum([command.find(x) == 0 for x in allowed_modules]):
        init_calm_env(params)
        result = eval(command+'(params)')
        result_b64 = base64.b64encode(json.dumps(result).encode()).decode()
        # TODO: add json safeguards
        print(f'result=[{result_b64}]')
    else:
        print('Command not found')


if __name__ == '__main__':
    main()
