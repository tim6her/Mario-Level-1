import time
import queue
import threading

from . import mqtt

class Button(object):
    def __init__(self, input_queue):
        self.input_queue = input_queue
        self._value = None

    @property
    def value(self):
        try:
            value = self.input_queue.get()
            return value
        except queue.Empty:
            return 0

    def __bool__(self):
        return self.value > 0


class Direction(Button):
    def __init__(self, input_queue, input_queue2):
        super(Direction, self).__init__(input_queue)
        self.input_queue2 = input_queue2
        self._init_value = None
        self._delta = None
        self._left = None
        self._right = None

    @property
    def value(self):
        try:
            angle = self.input_queue.get_nowait()
            sgn = self.input_queue2.get_nowait()
            self.input_queue2.put(sgn)
            value = (-1 + 2 * sgn) * angle
            print(value)
            return value
        except queue.Empty:
            return 0

    @property
    def delta(self):
        if self._init_value is None:
            self._init_value = self.value
            return 0
        return self._init_value - self.value

    @property
    def left(self):
        return self.delta < -1

    @property
    def right(self):
        return self.delta > 1

MOVE = Direction(mqtt.STEAR_QUEUE, mqtt.SGN_QUEUE)
JUMP = Button(mqtt.ACC_QUEUE)
ACTION = Button(mqtt.BRK_QUEUE)


THREAD = threading.Thread(target=mqtt.run_mqtt)
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
