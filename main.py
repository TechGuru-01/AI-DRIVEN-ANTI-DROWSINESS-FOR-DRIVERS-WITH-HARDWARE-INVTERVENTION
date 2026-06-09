from predrive_Evaluation import predriveEvaluator
from detection import LuminaDetection
from drive_interventions import DriveINTVN
from systModes import SystemMode
from lumina_Json import read_json, update_lockout
from lockout import lockoutManager
from nodemcu import NodeMCUStates

def start():
    detector = LuminaDetection(model="best.pt")
    node = NodeMCUStates(port="COM11", baudrate=115200)
    predrive_evaluator = predriveEvaluator(detector, node)

    lockout_data = read_json()
    lockout_time = lockout_data["lockout"]
    update_lockout()

    if lockout_time.get("lockout_reason") is not None and not lockout_time.get("lockout_handled", True):
        lockout = lockoutManager(detector)
        lockout.run_lockout()

    mode = predrive_evaluator.run_predrive()

    if mode == SystemMode.LOCKOUT.name:
        lockout = lockoutManager(detector)
        lockout.run_lockout()
    elif mode == SystemMode.DRIVE.name:
        drive = DriveINTVN(detector, node)
        drive.run()

if __name__ == "__main__":
    start()

 