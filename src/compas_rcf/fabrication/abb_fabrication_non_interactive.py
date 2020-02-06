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

IO_NEEDLES = 'doDNetOut1'

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
PICKING_BASE = Point(500.00, -750.00, 300.00)
BULLET_HEIGHT = 70

COMPRESSION_RATIO = .5


def get_picking_frames():

    pt = Point(0, 0, 0) + Vector(0, 0, BULLET_HEIGHT)
    picking_frame = Frame(pt, Vector(-1, 0, 0), Vector(0, 1, 0))

    offset_frame = picking_frame.copy()

    T = Translation([0, 0, BULLET_HEIGHT * .5])

    offset_frame.transform(T)

    return [picking_frame, offset_frame]


def adjust_placement_frame_with_compression_ratio(frame):
    T = Translation(frame.zaxis * BULLET_HEIGHT * COMPRESSION_RATIO)
    frame.transform(T)

    return frame


def get_offset_plane(frame):
    offset_z = BULLET_HEIGHT * .5
    offset_vector = Vector(0, 0, offset_z)

    placement_pt = frame.point
    xaxis = frame.xaxis
    yaxis = frame.yaxis

    offset_pt = placement_pt + offset_vector

    offset_frame = Frame(offset_pt, xaxis=xaxis, yaxis=yaxis)

    return offset_frame


if __name__ == '__main__':

    json_path = open_file_dialog()

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

    clay_bullets = load_bullets(json_path)

    # TODO: Iterate over objects instead of creating this extra step
    instructions = []
    for bullet in clay_bullets:
        instruction = {}
        instruction.update({'pre': bullet.pre_frames})
        instruction.update({'post': bullet.post_frames})
        instruction.update({'placement': bullet.placement_frame})
        instructions.append(instruction)

    for instruction in instructions:

        placement_frame = instruction['placement']
        pre_frames = instruction['pre']
        post_frames = instruction['post']

        # flip planes
        R = Rotation.from_axis_and_angle(placement_frame.xaxis, math.radians(180))

        placement_frame.transform(R)

        if not TARGET_REAL_ROBOT:
            # Custom instruction create a clay bullet in RobotStudio
            abb.send(CustomInstruction('r_A057_RS_Create_Bullet'))

        # change work object before picking
        abb.send(SetWorkObject(PICKING_WOBJ))

        # pick bullet
        picking_frame, offset_frame = get_picking_frames()

        abb.send(MoveToFrame(offset_frame, 500, Zone.FINE))

        abb.send_and_wait(MoveToFrame(picking_frame, 500, Zone.FINE))

        if TARGET_REAL_ROBOT:
            abb.send(SetDigital(IO_NEEDLES, 0))
        else:
            # Custom instruction can grip a bullet in RobotStudio note the tool tip must touch the bullet
            abb.send(CustomInstruction('r_A057_RS_ToolGrip'))

        abb.send(MoveToFrame(offset_frame, 500, Zone.FINE))

        # change work object before placing
        abb.send(SetWorkObject(PLACING_WOBJ))

        # add offset placing plane to pre and post frames
        adjusted_placement_for_compression = adjust_placement_frame_with_compression_ratio(placement_frame)

        offset_placing_plane = get_offset_plane(placement_frame)

        pre_frames.append(offset_placing_plane)
        post_frames.insert(0, offset_placing_plane)

        # Safe pos then vertical offset
        for frame in pre_frames:
            # TODO: Rotate frames in grasshopper instead
            frame.transform(R)
            abb.send(MoveToFrame(frame, 500, Zone.FINE))

        abb.send_and_wait(MoveToFrame(adjusted_placement_for_compression, 500, Zone.FINE))

        if TARGET_REAL_ROBOT:
            abb.send(SetDigital(IO_NEEDLES, 1))
        else:
            # Custom instruction releases a bullet from the tool
            abb.send(CustomInstruction('r_A057_RS_ToolRelease'))

        # offset placement frame then safety frame
        for frame in post_frames:
            # TODO: Rotate frames in grasshopper instead
            frame.transform(R)
            abb.send(MoveToFrame(frame, 500, Zone.FINE))

    abb.send(MoveToJoints(ROBOT_JOINTS_START_POSITION, EXTERNAL_AXIS_DUMMY, 1000, Zone.FINE))

    done = abb.send_and_wait(PrintText('Finished'))

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
