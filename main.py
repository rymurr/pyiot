from multiprocessing import Process, Queue
from pyiot.things import run_server
from pyiot.app import main

if __name__ == '__main__':
    print("in main", __name__)
    procs = list()
    queue = Queue()
    procs.append(Process(target=run_server, args=(queue, )))
    procs.append(Process(target=main, args=(queue, )))
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
