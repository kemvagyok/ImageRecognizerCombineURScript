from RobotArm import RobotArm
from ImageRecognizer import ImageRecognizer
from Cube import Cube

if __name__ == "__main__":
    imageRecognizer = ImageRecognizer(6,12)
    #robotArm = RobotArm('10.150.0.1', 'rtdeState.xml')
    #robotArm.start()
    #init
    front = imageRecognizer.checkingResult(f"Input/proba_1_12.jpg")[0]+1
    #robotArm.MoveByDirection("up")
    top = imageRecognizer.checkingResult(f"Input/proba_2_12.jpg")[0]+1
    cube = Cube(top, front)

    """while True:
        cmd = input("Which edge? ")
        if cmd == "exit":
            break
        moves = cube.pathBetweenTopAndEdge(cmd)
        for move in moves:
            cube.switchByDirection(move)
            robotArm.MoveByDirection(move)
    robotArm.interpreter.end_interpreter()
    robotArm.shutdown()"""
