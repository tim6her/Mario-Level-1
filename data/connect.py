import time
import queue
import threading

import requests

SIMULATE= False
IP_CAR = 'http://192.168.8.10'
IP_SIMULATOR = 'http://130.82.239.210'

ACCELERATOR = 'MO_Fahrpedalrohwert_01'
BREAK = 'ESP_Bremsdruck'
STEARING = 'LWI_VZ_Lenkradwinkel'
RPM = 'MO_Drehzahl_01'

ip = IP_SIMULATOR if SIMULATE else IP_CAR

MOVE_QUEUE = queue.LifoQueue()
JUMP_QUEUE = queue.LifoQueue()
ACT_QUEUE = queue.LifoQueue()

class Button(object):
    REQUEST_TEMP = '/signal/{}/value'

    def __init__(self, key, input_queue):
        self.key = key
        self.input_queue = input_queue
        self._value = 1

    @property
    def value(self):
        try:
            value = self.input_queue.get_nowait()
            print('Game', value)
            self.input_queue.put(value)
            return value
        except queue.Empty:
            return 0

    def __bool__(self):
        return self.value > 0

    def request(self):
        response = requests.get(ip + self.REQUEST_TEMP.format(self.key))
        value = response.json()['measurement']['value']
        value = value if value else 0
        return value

class Direction(Button):
    def __init__(self, key, input_queue):
        super(Direction, self).__init__(key, input_queue)
        self._last_value = 1
        self._delta = 1
        self._left = None
        self._right = None

    @property
    def delta(self):
        # if self._last_value is None:
        #     self._last_value = self.value
        #     return 0
        # return self._last_value - self.value
        return self.value

    @property
    def left(self):
        return self.delta < 0.5

    @property
    def right(self):
        return self.delta > 0.5

MOVE = Direction(STEARING, MOVE_QUEUE)
JUMP = Button(ACCELERATOR, JUMP_QUEUE)
ACTION = Button(BREAK, ACT_QUEUE)

def _main():
    while True:
        move = MOVE.request()
        MOVE_QUEUE.put(move)
        jump = JUMP.request()
        #print(jump)
        JUMP_QUEUE.put(jump)
        action = ACTION.request()
        ACT_QUEUE.put(action)
        time.sleep(0.01)

THREAD = threading.Thread(target=_main)
THREAD.daemon = True

if __name__ == '__main__':
    THREAD.start()

    for i in range(50):
        data = (JUMP.value, bool(JUMP),
                ACTION.value, bool(ACTION),
                MOVE.value, MOVE.left, MOVE.right)
        print(data)
        print(THREAD.is_alive())
        time.sleep(1)
