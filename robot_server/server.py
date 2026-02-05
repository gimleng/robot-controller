from flask import Flask

app = Flask(__name__)


def forward():
    print("FORWARD")


def backward():
    print("BACKWARD")


def left():
    print("LEFT")


def right():
    print("RIGHT")


def cw():
    print("CLICKWISE")


def ccw():
    print("COUNTERCLICKWISE")


def stop():
    print("STOP")


@app.route("/move/<cmd>")
def move(cmd):
    actions = {
        "forward": forward,
        "backward": backward,
        "left": left,
        "right": right,
        "stop": stop,
        "cw": cw,
        "ccw": ccw,
    }

    if cmd in actions:
        actions[cmd]()
        return "OK"
    return "INVALID", 400


app.run(host="0.0.0.0", port=5000, threaded=True)
