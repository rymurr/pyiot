from urllib.parse import quote
import os

from azure.eventhub import EventHubClient, EventData

URL = 'rymurr-iottest.servicebus.windows.net'
EVENTHUB = 'testiotrymurr'
KEY = os.environ.get('PYIOT_EVENTHUB_KEY', 'oh-no!')
ADDRESS = 'amqps://' + 'sendtestiot' + ':' + quote(
    KEY) + '@' + URL + '/' + EVENTHUB


def to_azure(events):
    client = EventHubClient(ADDRESS, debug=True)
    sender = client.add_sender(partition="0")
    client.run()
    try:
        for event in events:
            sender.send(EventData(event))
    except:
        raise
    finally:
        client.stop()
