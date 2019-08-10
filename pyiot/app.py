from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from dateutil.parser import parse
import time
from flask import Flask, request
from prometheus_client import generate_latest, REGISTRY, Gauge, Info
from .constants import names
from .csv import write
from .yocto import yocto_data

gauges = {}


def main(queue=None):
    software = Info('wunderground_software', 'software')
    app = Flask(__name__)

    def get_gauge(name, prefix='wunderground_'):
        if name in gauges:
            return gauges[name]
        gauge = Gauge(prefix + name, names.get(name, name))
        gauges[name] = gauge
        return gauge

    @app.route('/metrics', methods=['GET'])
    def metrics():
        return generate_latest(REGISTRY), 200

    @app.route('/esp')
    def esp():
        vals = []
        names = ['temp', 'light', 'pressure', 'humidity', 'time']
        for name in names:
            if name == 'time':
                value = int(time.time())
            else:
                value = request.args[name]
            if queue:
                queue.put(('acorn', name, value))
            get_gauge(name, 'acorn_').set(value)
            vals.append(value)
        write(vals, 'acorn', names)
        return "OK", 200

    @app.route('/', methods=['POST'])
    def yocto():
        data = request.data
        val_dict, time = yocto_data(data)
        for name, value in val_dict.items():
            if queue:
                queue.put(('yocto', name, value))
            get_gauge(name, '').set(value)
            write([name, value, time], 'yocto', ['name', 'value', 'timestamp'])
        return "OK", 200

    @app.route('/weatherstation/updateweatherstation.php')
    def wunderground():
        vals = []
        for name in names:
            value = request.args[name] if name != 'dateutc' else parse(
                request.args[name]).timestamp()
            if queue:
                queue.put(('ambientweather', name, value))
            get_gauge(name).set(value)
            vals.append(value)
        write(vals, 'ambientweather', names)
        software.info({'software_name': request.args['softwaretype']})
        return "OK", 200

    print('starting flask server')
    app.run(debug=False, port=9090, host='0.0.0.0')
