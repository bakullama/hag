from flask import Flask
import random
import time
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mean = 1
sd = 3

class Status(object):
    unknown = 'unknown'
    building = 'BUILDING'
    success = 'SUCCESS'
    failure = 'FAILURE'


class Commands(object):
    start = 'START'
    restart = 'RESTART'



box_states = {
    'testaut-1-stb-1': Status.unknown,
    'testaut-1-stb-2': Status.unknown,
    'testaut-1-stb-3': Status.unknown,
    'testaut-1-stb-4': Status.unknown,
}
box_times = {
    'testaut-1-stb-1': 0,
    'testaut-1-stb-2': 0,
    'testaut-1-stb-3': 0,
    'testaut-1-stb-4': 0,
}

app = Flask(__name__)


@app.route("/fake-jenkins-status/<slot>")
def status(slot):
    time.sleep(0.2)# server response time
    if box_states[slot] == Status.building:
        if time.time() - box_times[slot] > random.choice([0.5, 1, 1, 1, 2, 2, 5]):
            box_states[slot] = random.choice(
                [Status.success] + [Status.failure] * 3)
    return box_states[slot]


@app.route("/fake-jenkins-do-something/<whut>/<slot>")
def do_something(whut, slot):
    if whut == Commands.start:
        box_states[slot] = Status.building
        box_times[slot] = time.time()
    elif whut == Commands.restart:
        box_states[slot] = Status.unknown
        box_times[slot] = 0

    return str(box_times[slot])


if __name__ == '__main__':
    app.run(port=4000)


