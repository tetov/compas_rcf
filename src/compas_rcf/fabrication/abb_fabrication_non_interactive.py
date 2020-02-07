""" From compas_rcc_course/03_RRC_Custom/Python/compas_rrc_custom_B_pick_and_place_challenge.py
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import Vector
from compas_fab.backends.ros import RosClient
from compas_rrc import AbbClient
from compas_rrc import CustomInstruction
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import Zone

from compas_rcf.utils.json_ import load_bullets
from compas_rcf.utils.ui import open_file_dialog

# ROBOT SETUP
TARGET_REAL_ROBOT = False

TOOL = 't_A057_MockTool01'
PICKING_WOBJ = 'ob_A057_WobjPicking01'
PLACING_WOBJ = 'ob_A057_WobjPlacing01'

# IO
IO_NEEDLES = 'doDNetOut1'
GRIP = 1
RELEASE = 0

# Acceleration
ACCEL = 100  # %
ACCEL_RAMP = 100  # %: The rate at which acceleration and deceleration increases as a percentage of the normal values.

# Max Speed
SPEED_OVERRIDE = 100  # %
SPEED_MAX_TCP = 500  # mm/2

# Safe positions
ROBOT_JOINTS_START_POSITION = [10.7, 38.48, 21.43, -366.76, 32.8, 61.32]
ROBOT_JOINTS_END_POSITION = ROBOT_JOINTS_START_POSITION

# Define external axis
EXTERNAL_AXIS_DUMMY = []

# FABRICATION SETUP
OFFSET_DISTANCE = 100  # mm

def get_picking_frame(bullet_height):
    """ Get picking frame
    """
    # TODO: Set up a grid to pick from
    picking_frame = Frame(Point(0, 0, 0), Vector(-1, 0, 0), Vector(0, 1, 0))

    return get_offset_frame(picking_frame, bullet_height)



def get_offset_frame(origin_frame, distance):
    """ Offset a frame in it's Z axis direction
    """
    offset_vector = origin_frame.zaxis * distance
    T = Translation(offset_vector)

    return origin_frame.transformed(T)

def send_grip_release(do_state):
    if TARGET_REAL_ROBOT:
        abb.send(SetDigital(IO_NEEDLES, do_state))
    else:
        # Custom instruction can grip a bullet in RobotStudio note the tool tip must touch the bullet
        if do_state == GRIP:
            abb.send(CustomInstruction('r_A057_RS_ToolGrip'))
        else:
            abb.send(CustomInstruction('r_A057_RS_ToolRelease'))

if __name__ == '__main__':

    json_path = open_file_dialog()
    print(json_path)
    clay_bullets = load_bullets(json_path)
    print(clay_bullets)

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    abb.send(SetTool(TOOL))
    abb.send(SetWorkObject(PLACING_WOBJ))

    # Set Acceleration
    abb.send(SetAcceleration(ACCEL, ACCEL_RAMP))

    # Set Max Speed
    abb.send(SetMaxSpeed(SPEED_OVERRIDE, SPEED_MAX_TCP))

    print('Tool, Wobj, Acc and MaxSpeed sent to robot')

    # Initial configuration
    abb.send(MoveToJoints(ROBOT_JOINTS_START_POSITION, EXTERNAL_AXIS_DUMMY, 500, Zone.FINE))


    for bullet in clay_bullets:

        placement_frame = bullet.placement_frame
        pre_frames = bullet.pre_frames
        post_frames = bullet.post_frames

        bullet_height = bullet.height
        compressed_height = bullet.compressed_height

        if not TARGET_REAL_ROBOT:
            # Custom instruction create a clay bullet in RobotStudio
            # TODO: Create bullet at picking point
            abb.send(CustomInstruction('r_A057_RS_Create_Bullet'))

        # change work object before picking
        abb.send(SetWorkObject(PICKING_WOBJ))

        # pick bullet
        picking_frame = get_picking_frame(bullet_height)
        offset_picking = get_offset_frame(picking_frame, OFFSET_DISTANCE)

        abb.send(MoveToFrame(offset_picking, 500, Zone.FINE))

        abb.send_and_wait(MoveToFrame(picking_frame, 500, Zone.FINE))
        # TODO: Try compress bullet a little bit before picking

        send_grip_release(GRIP)

        abb.send(MoveToFrame(offset_picking, 500, Zone.FINE))

        # change work object before placing
        abb.send(SetWorkObject(PLACING_WOBJ))

        # add offset placing plane to pre and post frames

        offset_placement = get_offset_frame(placement_frame, OFFSET_DISTANCE)

        # Safe pos then vertical offset
        for frame in pre_frames:
            abb.send(MoveToFrame(frame, 500, Zone.FINE))

        abb.send(MoveToFrame(offset_placement, 500, Zone.FINE))
        abb.send_and_wait(MoveToFrame(placement_frame, 500, Zone.FINE))

        send_grip_release(RELEASE)

        abb.send(MoveToFrame(offset_placement, 500, Zone.FINE))

        # offset placement frame then safety frame
        for frame in post_frames:
            abb.send(MoveToFrame(frame, 500, Zone.FINE))

        # REPEAT LOOP

    abb.send(MoveToJoints(ROBOT_JOINTS_START_POSITION, EXTERNAL_AXIS_DUMMY, 1000, Zone.FINE))

    done = abb.send_and_wait(PrintText('Finished'))

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
