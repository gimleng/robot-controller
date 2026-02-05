from flask import Flask
import rospy
from geometry_msgs.msg import Twist

app = Flask(__name__)

# --- ROS init ---
rospy.init_node("flask_cmd_vel_server", anonymous=True)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

current_speed = 0.2
MAX_SPEED = 0.9
MIN_SPEED = 0.1
STEP = 0.1

def send_cmd(x=0, y=0, theta=0):
    msg = Twist()
    msg.linear.x = x
    msg.linear.y = y
    msg.angular.z = theta
    pub.publish(msg)

@app.route("/move/<cmd>")
def move(cmd):
    if cmd == "forward":
        send_cmd(x=current_speed)
    elif cmd == "backward":
        send_cmd(x=-current_speed)
    elif cmd == "left":
        send_cmd(y=current_speed)
    elif cmd == "right":
        send_cmd(y=-current_speed)
    elif cmd == "cw":
        send_cmd(theta=-0.5)
    elif cmd == "ccw":
        send_cmd(theta=0.5)
    elif cmd == "stop":
        send_cmd()
    else:
        return "INVALID", 400

    return "OK"

@app.route("/speed/up")
def speed_up():
    global current_speed
    current_speed += STEP
    if current_speed > MAX_SPEED:
        current_speed = MAX_SPEED
    rospy.loginfo(f"Speed up: {current_speed}")
    return str(current_speed)


@app.route("/speed/down")
def speed_down():
    global current_speed
    current_speed -= STEP
    if current_speed < MIN_SPEED:
        current_speed = MIN_SPEED
    rospy.loginfo(f"Speed down: {current_speed}")
    return str(current_speed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
