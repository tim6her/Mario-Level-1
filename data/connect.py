import time

import requests

SIMULATE= True
IP_CAR = 'http://192.168.8.10'
IP_SIMULATOR = 'http://130.82.239.210'

ACCELERATOR = 'MO_Fahrpedalrohwert_01'
BREAK = 'ESP_Fahrer_bremst'
STEARING = 'LWI_Lenkradwinkel'
RPM = 'MO_Drehzahl_01'

ip = IP_SIMULATOR if SIMULATE else IP_CAR

class Button(object):
    REQUEST_TEMP = '/signal/{}/value'

    def __init__(self, key):
        self.key = key
        self._value = None

    @property
    def value(self):
        response = requests.get(ip + self.REQUEST_TEMP.format(self.key))

        return response.json()['measurement']['value']

    def __bool__(self):
        return bool(self.value)

class Direction(Button):
    def __init__(self, key):
        super(Direction, self).__init__(key)
        self._last_value = None
        self._delta = None
        self._move = None

    @property
    def delta(self):
        if self._last_value is None:
            self._last_value = self.value
            return 0
        delta = self._last_value - self.value
        self._last_value -= delta
        return delta

    @property
    def move(self):
        sign = lambda x: x and (1, -1)[x < 0]
        return sign(self.delta)


MOVE = Direction(STEARING)
ACTION = Button(ACCELERATOR)
JUMP = Button(BREAK)

if __name__ == '__main__':
    for i in range(50):
        print(ACCELERATOR, bool(JUMP))
        print(STEARING, MOVE.value)
        print(STEARING, MOVE.move)
        time.sleep(0.1)
