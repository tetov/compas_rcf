"""Classes for custom RAPID instructions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rrc import PrintText
from compas_rrc import Stop
from compas_rrc.common import FeedbackLevel

INSTRUCTION_PREFIX = "r_A057_"


class PrintTextNoErase(PrintText):
    """Print text on the controller pendant, without first clearing the screen.

    RAPID Instruction: TPWrite
    """

    def __init__(self, text, feedback_level=FeedbackLevel.NONE):
        super(PrintTextNoErase, self).__init__(text, feedback_level=feedback_level)
        self.instruction = INSTRUCTION_PREFIX + "TPWriteNoErase"


class StopAll(Stop):
    r"""StopAll is a call that stops all motion tasks from the robot.

    RAPID Instruction: Stop \AllMoveTasks;
    """

    def __init__(self, feedback_level=FeedbackLevel.NONE):
        super(StopAll, self).__init__(feedback_level=feedback_level)
        self.instruction = INSTRUCTION_PREFIX + "StopAll"
