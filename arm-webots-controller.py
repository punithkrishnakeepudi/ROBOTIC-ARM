from controller import Robot
import socket
import math

# =======================
# CONFIG
# =======================
UDP_PORT = 4210
BUFFER_SIZE = 1024

# =======================
# INIT WEBOTS
# =======================
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Get motors
motor_names = [
    "base_joint",
    "shoulder_joint",
    "elbow_joint",
    "wrist_pitch_joint",
    "wrist_roll_joint",
    "gripper_joint"
]

motors = []

for name in motor_names:
    motor = robot.getDevice(name)
    motor.setPosition(0.0)
    motor.setVelocity(2.0)
    motors.append(motor)

print("Motors initialized.")

# =======================
# UDP SERVER
# =======================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))
sock.setblocking(False)

print("Listening for UDP commands on port", UDP_PORT)

# =======================
# ANGLE CONVERSION
# =======================
def degree_to_radian(deg):
    return math.radians(deg)

def map_gripper(deg):
    # Your real servo 0-90 maps to 0-0.8 rad in Webots
    return (deg / 90.0) * 0.8

# =======================
# MAIN LOOP
# =======================
while robot.step(timestep) != -1:

    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode().strip()

        if message.startswith("S"):
            parts = message[1:].split(":")
            servo_id = int(parts[0])
            angle = int(parts[1])

            print(f"Received -> Servo {servo_id}: {angle}")

            if 0 <= servo_id < 6:

                if servo_id == 5:
                    position = map_gripper(angle)
                else:
                    position = degree_to_radian(angle - 90)

                motors[servo_id].setPosition(position)

    except BlockingIOError:
        pass
