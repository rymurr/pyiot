import json
import time as _time


def yocto_data(data):
    results = {}
    obj = json.loads(data)
    time = obj['/api.json'].get('realTimeClock', {'unixTime': int(_time.time())})['unixTime']
    parse_keys = [i for i in obj.keys() if '/bySerial' in i]
    for key in parse_keys:
        measurements = obj[key]
        if 'module' in measurements:
            name = measurements['module']['logicalName'].replace('-', '')
        else:
            name = 'unknown'
        for module in [i for i in measurements if i not in {'module', 'dataLogger'}]:
            sensor_data = measurements[module]
            results['_'.join([name, module])] = sensor_data['advertisedValue']
        results['_'.join([name, 'unix_time'])] = time
    return results
