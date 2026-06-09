import json
import os 
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from systModes import SystemMode

LUMINA_STATUS = "Lumina.json"

def get_timestamp():
    manila_time = datetime.now(ZoneInfo("Asia/Manila"))
    timestamp = manila_time.strftime("%Y-%m-%d %I:%M:%S %p")
    return timestamp

def read_json():
    if not os.path.exists(LUMINA_STATUS):
        return {
            "users": [],
            "contacts": [],
            "lockout": { "timestamp": None, "lockout_reason": None, "attempts": 0, "lockout_handled": True }
        }

    try:
        with open(LUMINA_STATUS, "r") as f:
            data = json.load(f)

            if "lockout" not in data:
                data["lockout"] = {
                    "timestamp": None, "lockout_reason": None, "attempts": 0, "lockout_handled": True
                }
            lockout = data["lockout"]

        if lockout.get("timestamp"):
            if isinstance(lockout["timestamp"], str):
                dt = datetime.strptime(lockout["timestamp"], "%Y-%m-%d %I:%M:%S %p")
                dt = dt.replace(tzinfo=ZoneInfo("Asia/Manila"))
                
        if "lockout_handled" not in lockout:
            lockout["lockout_handled"] = False
        return data
    except:
        return {
            "users": [],
            "contacts": [],
            "lockout": {"timestamp": None, "lockout_reason": None, "attempts": 0, "lockout_handled": True}
        }


def write_json(data):
    with open(LUMINA_STATUS, "w") as f:
        json.dump(data, f, indent=4)

def is_expired(last_timestamp_str, cooldown_seconds=3600):
    dt = datetime.strptime(last_timestamp_str, "%Y-%m-%d %I:%M:%S %p")
    dt = dt.replace(tzinfo=ZoneInfo("Asia/Manila"))
    now = datetime.now(ZoneInfo("Asia/Manila"))
    return (now - dt).total_seconds() >= cooldown_seconds

def is_lockout_active():
    data = read_json()
    lockout = data["lockout"]
    if not lockout["timestamp"]:
        return False
    return not is_expired(lockout["timestamp"])

def update_lockout(lockout_reason=None, attempts=None, lockout_handled=None, mode=None):
    data = read_json()
    lockout = data["lockout"]

    now_dt = datetime.now(ZoneInfo("Asia/Manila"))
    now_str = now_dt.strftime("%Y-%m-%d %I:%M:%S %p")

    if lockout.get("first_attempt") is None:
        lockout["first_attempt"] = now_str

    if lockout.get("first_attempt") is None or is_expired(lockout["first_attempt"], cooldown_seconds=3600):
        lockout["attempts"] = 0
        lockout["lockout_reason"] = None
        lockout["lockout_handled"] = True
        lockout["first_attempt"] = now_str
    else:
        if mode == SystemMode.LOCKOUT.name and attempts is None:
            lockout["attempts"] = lockout.get("attempts", 0) + 1
        elif attempts is not None:
            lockout["attempts"] = attempts

        if mode == SystemMode.LOCKOUT.name and (attempts is None or attempts != lockout.get("attempts", 0)):
            lockout["timestamp"] = now_str

    if lockout_reason:
        lockout["lockout_reason"] = lockout_reason
    if lockout_handled is not None:
        lockout["lockout_handled"] = lockout_handled

    write_json(data)
    return data