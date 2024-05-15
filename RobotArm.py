from rtdeState import RtdeState
from Dashboard import Dashboard
import sendInterpreterFromFile as sendFile
from interpreter.interpreter import InterpreterHelper
import logging
import sys

class RobotArm:
    def __init__(self, robot_host, rtde_config):
        self.dash = Dashboard(robot_host)
        self.rState = RtdeState(robot_host, rtde_config, frequency=500)
        self.interpreter = InterpreterHelper(robot_host)

    def robot_boot(self):
        # Check to make sure robot is in remote control.
        remoteCheck = self.dash.sendAndReceive('is in remote control')
        if 'false' in remoteCheck:
            logging.error('Robot is in local mode. Cannot issue system commands. Exiting...')
            self.shutdown()
            sys.exit()
        # Check robot mode and boot if necessary.
        powermode = self.dash.sendAndReceive('robotmode')
        if 'POWER_OFF' in powermode:
            logging.info('Attempting to power robot and release brakes.')
            logging.info(self.dash.sendAndReceive('brake release'))
            temp_state = self.rState.receive()
            bootStatus = temp_state.robot_mode
            # Grab robot mode from RTDE and loop until robot fully boots. Monitor safety state
            # and exit if safety state enters a non-normal mode.
            while bootStatus != 7:
                temp_state = self.rState.receive()
                bootStatus = temp_state.robot_mode
                safetyStatus = temp_state.safety_status
                if safetyStatus != 1:
                    logging.error('Robot could not boot successfully. Exiting...')
                    self.shutdown()
                    sys.exit()
            logging.info('Robot booted succesfully. Ready to run.')

    def shutdown(self):
        self.dash.close()
        self.rState.con.send_pause()
        self.rState.con.disconnect()

    def startRobotProgram(self, fileName):
        # Check to see if currently loaded program is Interpret.urp
        currentProgram = self.dash.sendAndReceive('get loaded program')
        # Users should add error handling in case program load fails.
        if not currentProgram.endswith(f'{fileName}'):
            self.dash.sendAndReceive(f'load {fileName}')
            logging.info(f'Found and loaded {fileName}')
        else:
            logging.info(f'{fileName} already loaded.')
        self.dash.sendAndReceive('play')
        # Check program status via RTDE and wait until it returns a "Playing" state.
        temp_state = self.rState.receive()
        startStatus = temp_state.runtime_state
        while startStatus != 2:
            temp_state = self.rState.receive()
            startStatus = temp_state.runtime_state
        logging.info('Playing program')

    def start(self):
        self.dash.connect()
        self.rState.initialize()
        self.robot_boot()
        self.interpreter.connect()
        self.startRobotProgram('gripper_test.urp')

    def MoveArmUpLine(self):
        sendFile.send_cmd_interpreter_mode_file(self.interpreter, 'MoveUpLine.txt')

    def MoveArmBackLine(self):
        sendFile.send_cmd_interpreter_mode_file(self.interpreter, 'MoveBackLine.txt')

    def MoveArmLeftRotation(self):
        sendFile.send_cmd_interpreter_mode_file(self.interpreter, 'MoveLeftRotation.txt')

    def MoveArmRightRotation(self):
        sendFile.send_cmd_interpreter_mode_file(self.interpreter, 'MoveRightRotation.txt')

    def MoveByDirection(self, direction):
        if direction == "up":
            self.MoveArmUpLine()
        if direction == "down":
            self.MoveArmBackLine()
        if direction == "left":
            self.MoveArmLeftRotation()
            self.MoveArmBackLine()
            self.MoveArmLeftRotation()

        if direction == "right":
            self.MoveArmLeftRotation()
            self.MoveArmUpLine()
            self.MoveArmRightRotation()
