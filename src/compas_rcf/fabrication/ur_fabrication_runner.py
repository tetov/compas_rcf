"""Not ready yet
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import socket
import time
from pathlib import Path

from compas_rcf.ur.helpers import turn_off_outputs_program
from compas_rcf.ur.urscript_wrapper import movel
from compas_rcf.ur.urscript_wrapper import set_DO
from compas_rcf.ur.urscript_wrapper import set_TCP
from compas_rcf.ur.urscript_wrapper import socket_close
from compas_rcf.ur.urscript_wrapper import socket_open
from compas_rcf.ur.urscript_wrapper import socket_send_string
from compas_rcf.ur.urscript_wrapper import textmsg
from compas_rcf.utils.database import get_bullets

# ===============================================================

# GLOBALS
# ===============================================================

DEBUG = False

FILE_DIR = Path(__file__).parent.absolute()
REPO_PATH = Path(__file__).parents[2].absolute()
FILE_NAME = "commands_group_04.json"
SERVER_ADDRESS = "192.168.10.11"
SERVER_PORT = 30003
UR_IP = "192.168.10.10"
UR_SERVER_PORT = 30002

ROBOT_L_SPEED = 0.6  # m/s
ROBOT_ACCEL = 0.8  # m/s2
ROBOT_SAFE_SPEED = .8
ROBOT_J_SPEED = .8
ZONING = 0.  # m

AIR_PRESSURE_DO = 0

UR_PROGRAM_FOOTER = ""
UR_PROGRAM_FOOTER += socket_open(SERVER_ADDRESS, SERVER_PORT)
UR_PROGRAM_FOOTER += textmsg("End program")
UR_PROGRAM_FOOTER += socket_send_string("Script finished")
UR_PROGRAM_FOOTER += socket_close()
UR_PROGRAM_FOOTER += "end\n"
UR_PROGRAM_FOOTER += "program()\n"

# ===============================================================

# UTIL
# ===============================================================

LOG_FILE = Path.joinpath(FILE_DIR, "main_direct_send_group_04.log")
UR_SCRIPT_LOG = Path.joinpath(FILE_DIR, "main_direct_send_group_04.ur_log.log")
logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s")


def start_log() -> None:
    logging.debug("Start script")
    logging.debug("GLOBALS")
    logging.debug("FILE_DIR: {}".format(FILE_DIR))
    logging.debug("REPO_PATH: {}".format(REPO_PATH))
    logging.debug("FILE_NAME: {}".format(FILE_NAME))
    logging.debug("SERVER_ADDRESS: {}".format(SERVER_ADDRESS))
    logging.debug("SERVER_PORT: {}".format(SERVER_PORT))
    logging.debug("UR_IP: {}".format(UR_IP))
    logging.debug("UR_SERVER_PORT: {}".format(UR_SERVER_PORT))
    logging.debug("AIR_PRESSURE_DO: {}".format(AIR_PRESSURE_DO))


# ===============================================================

# PARSE COMMANDS FROM JSON
# ===============================================================


def parse_json(file_name):
    file = Path.joinpath(FILE_DIR.parent, file_name)

    with file.open(mode='r') as f:
        data = json.load(f)

    start_at_safe_pt = data['start_at_safe_pt']
    len_command = data['len_command']
    gh_commands = data['gh_commands']

    commands = format_commands(gh_commands, len_command)

    # validate_commands(commands)

    print("We have %d commands to send" % len(commands))

    return commands, start_at_safe_pt


# ===============================================================

# UR SCRIPT COMMANDS
# ===============================================================

# ===============================================================

# ===============================================================

# UR SCRIPT PROGRAMS
# ===============================================================


def generate_bullet_placing_program(bullet):
    script = []
    script += "def program():\n"
    script += set_TCP(bullet.tcp)

    for i, frame in enumerate(bullet.pre_frames):
        script += movel(frame, accel=ROBOT_ACCEL, speed=ROBOT_L_SPEED, radius=ZONING)

    script += movel(bullet.placement_frame, accel=ROBOT_ACCEL, speed=ROBOT_L_SPEED, radius=ZONING)
    script += set_DO(AIR_PRESSURE_DO, True)
    script += textmsg("Air pressure on")

    for i, frame in enumerate(bullet.post_frames):
        script += movel(frame, accel=ROBOT_ACCEL, speed=ROBOT_L_SPEED, radius=ZONING)

    script += UR_PROGRAM_FOOTER

    if DEBUG:
        with open(UR_SCRIPT_LOG, mode='w') as f:
            f.write(script.decode('utf-8'))

    return script


# ===============================================================

# ===============================================================


def main() -> None:
    start_log()

    bullets = get_bullets()

    send_socket = socket.create_connection((UR_IP, UR_SERVER_PORT), timeout=2)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.debug("Sockets setup")

    # make server
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    recv_socket.bind((SERVER_ADDRESS, SERVER_PORT))

    for bullet in bullets:
        script = generate_bullet_placing_program(bullet)

        print("Sending placing commands for bullet id {}".format(bullet.id))

        # send file
        script = script.encode()
        send_socket.send(script)
        logging.debug("File sent")

        # Listen for incoming connections
        recv_socket.listen(1)
        while True:
            logging.debug("Waiting for accept")
            connection, client_address = recv_socket.accept()
            logging.debug("Received accept from: {}".format(client_address))
            break

    recv_socket.close()

    script = turn_off_outputs_program()

    send_socket.send(script)

    time.sleep(5)

    send_socket.close()
    print("Program done ...")


if __name__ == "__main__":
    main()
