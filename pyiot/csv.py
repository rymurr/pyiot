import os
import datetime


def get_file(name, headers=None):
    file_path = os.environ.get('PYIOT_PATH', os.path.expanduser("~"))
    date = datetime.datetime.utcnow().strftime('%Y%m%d')
    filename = 'pyiot-' + name + '-' + date + '.csv'
    file = os.path.join(file_path, filename)
    if os.path.exists(file):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    f = open(file, append_write)
    if append_write == 'w' and headers:
        f.write(','.join(headers))
        f.write('\n')

    return f


def write(row, name, headers=None):
    string = ','.join([str(i) for i in row]) + '\n'
    with get_file(name, headers) as f:
        f.write(string)
