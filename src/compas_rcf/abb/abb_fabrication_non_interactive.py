""" From compas_rcc_course/03_RRC_Custom/Python/compas_rrc_custom_B_pick_and_place_challenge.py
"""
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector

from compas_fab.backends.ros import RosClient

from compas_rrc import AbbClient
from compas_rrc import CustomInstruction
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import SetAcceleration
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import Zone
from compas_rrc import SetDigital

# ROBOT SETUP
TARGET_REAL_ROBOT = False

TOOL = 't_A057_MockTool01'
WORK_OBJ = 'ob_A057_Wobj01'

IO_NEEDLES = 'IONeedles????'

# Acceleration
ACCEL = 100  # %
ACCEL_RAMP = 100  # %: The rate at which acceleration and deceleration increases as a percentage of the normal values.

# Max Speed
SPEED_OVERRIDE = 100  # %
SPEED_MAX_TCP = 500  # mm/2

# Safe positions
ROBOT_JOINTS_START_POSITION = [0.0, 10., 50., 0.0, 60., 0.]
ROBOT_JOINTS_END_POSITION = ROBOT_JOINTS_START_POSITION

# Define external axis
EXTERNAL_AXIS_DUMMY = []

# FABRICATION SETUP
PICKING_BASE = Point(500.00, -750.00, 300.00)
BULLET_HEIGHT = 180

COMPRESSION_RATIO = .5


def picking_frame():
    pt = PICKING_BASE + Vector(0, 0, BULLET_HEIGHT)
    frame = Frame(pt, Vector(-1, 0, 0), Vector(0, 1, 0))
    return frame


def placing_frames(pt):
    placing_frame = Frame(pt, Vector(-1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))
    pre_frame = Frame(pt + Vector(0, 0, BULLET_HEIGHT + 200), Vector(-1, 0, 0), Vector(0, 1, 0))
    post_frame = pre_frame

    return [pre_frame, placing_frame, post_frame]


if __name__ == '__main__':

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    abb.send(SetTool(TOOL))
    abb.send(SetWorkObject(WORK_OBJ))

    # Set Acceleration
    abb.send(SetAcceleration(ACCEL, ACCEL_RAMP))

    # Set Max Speed
    abb.send(SetMaxSpeed(SPEED_OVERRIDE, SPEED_MAX_TCP))

    # User message -> basic settings send to robot
    print('Tool, Wobj, Acc and MaxSpeed sent to robot')

    # Define frames
    picking_frame = picking_frame()

    # End of Code

    for i in range(20):
        if not TARGET_REAL_ROBOT:
            # Custom instruction create a clay bullet in RobotStudio
            abb.send(CustomInstruction('r_A057_RS_Create_Bullet'))

        # Safe start pos
        abb.send(MoveToJoints(ROBOT_JOINTS_START_POSITION, EXTERNAL_AXIS_DUMMY, 1000, Zone.FINE))

        # Define placing frame
        placing_pt = Point(400, 400 + 100 * i, BULLET_HEIGHT * COMPRESSION_RATIO)
        pre_frame, placing_frame, post_frame = placing_frames(placing_pt)

        # Go to picking
        abb.send_and_wait(MoveToFrame(picking_frame, 500, Zone.FINE))

        if TARGET_REAL_ROBOT:
            abb.send(SetDigital(IO_NEEDLES, 0))
        else:
            # Custom instruction can grip a bullet in RobotStudio note the tool tip must touch the bullet
            abb.send(CustomInstruction('r_A057_RS_ToolGrip'))

        # Safe pos
        abb.send(MoveToJoints(ROBOT_JOINTS_START_POSITION, EXTERNAL_AXIS_DUMMY, 1000, Zone.FINE))

        # Placing pos
        abb.send(MoveToFrame(pre_frame, 500, Zone.FINE))
        abb.send_and_wait(MoveToFrame(placing_frame, 500, Zone.FINE))

        if TARGET_REAL_ROBOT:
            abb.send(SetDigital(IO_NEEDLES, 1))
        else:
            # Custom instruction releases a bullet from the tool
            abb.send(CustomInstruction('r_A057_RS_ToolRelease'))

        abb.send(MoveToFrame(post_frame, 500, Zone.FINE))

    abb.send(MoveToJoints(ROBOT_JOINTS_START_POSITION, EXTERNAL_AXIS_DUMMY, 1000, Zone.FINE))

    done = abb.send_and_wait(PrintText('Finished'))

    # End of Code
    print('Finished')

    # Close client
    abb.close()
    abb.terminate()
