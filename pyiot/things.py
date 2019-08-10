from __future__ import division, print_function
from webthing import MultipleThings, Property, Thing, Value, WebThingServer
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
import logging


class AmbientWeather(Thing):
    """A weather sensor which updates its measurement every few seconds."""

    def __init__(self):
        Thing.__init__(self, 'ObserverIP Weather Sensor', ['MultiLevelSensor'],
                       'A web connected weather sensor')

        self.humidity = Value(0.0)
        self.add_property(
            Property(self,
                     'humidity',
                     self.humidity,
                     metadata={
                         '@type': 'LevelProperty',
                         'title': 'Humidity',
                         'type': 'number',
                         'description': 'The current humidity in %',
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'percent',
                         'readOnly': True,
                     }))

    def put(self, name, value, loop):
        if name == 'humidity':
            def alert(prop, value):
                prop.notify_of_external_update(value)

            loop.add_callback(alert, self.humidity, value)


class Yocto(Thing):
    """A weather sensor which updates its measurement every few seconds."""

    def __init__(self):
        Thing.__init__(self, 'Yoctopuce Sensors', ['MultiLevelSensor'],
                       'A web connected weather sensor')

        self.humidity = Value(0.0)
        self.add_property(
            Property(self,
                     'humidity',
                     self.humidity,
                     metadata={
                         '@type': 'LevelProperty',
                         'title': 'Humidity',
                         'type': 'number',
                         'description': 'The current humidity in %',
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'percent',
                         'readOnly': True,
                     }))

    def put(self, name, value, loop):
        if name == 'humidity':
            def alert(prop, value):
                prop.notify_of_external_update(value)

            loop.add_callback(alert, self.humidity, value)


def consumer(queue, response_map, loop):
    print("entering consumer")
    if queue is None:
        print("no queue!")
    while True:
        item = queue.get()
        if item is None:
            break
        response_item = response_map[item[0]]
        if response_item:
            response_item.put(item[1], item[2], loop)


def run_server(queue=None):
    things = [AmbientWeather(), Yocto()]
    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings(things, 'IoTSensors'),
                            port=8088,
                            hostname="beagle.rymurr.com")
    try:
        logging.info('starting the server')

        executor = ThreadPoolExecutor(max_workers=1)
        IOLoop.current().run_in_executor(executor, consumer, queue,
                                         {'ambientweather': things[0], 'yocto': things[1]},
                                         IOLoop.current())
        #       executor.submit(consumer, queue, {'ambientweather': things[0]})
        print("starting things server")
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')
