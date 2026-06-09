import time
from systModes import State

class DriverStates:
    def __init__(self, awake_time=None, drowsy_time=None, yawn_time=None, awake_trans=2.5, drowsy_trans=2.5, yawn_trans=2.5):
        self.idle_state = State.NO_DRIVER
        self.state_0 = State.AWAKE
        self.state_1 = State.DROWSY
        self.state_2 = State.YAWNING
        self.curr_state = self.state_0
        self.awake_time = awake_time
        self.awake_trans = awake_trans
        self.drowsy_time = drowsy_time
        self.drowsy_trans = drowsy_trans
        self.yawn_time = yawn_time
        self.yawn_trans = yawn_trans
        self.last_cls = None
        self.non_drowsy_count = 0

    def awake_to_other_states(self, cls):
        if self.curr_state == self.state_0:
            if cls == 1:
                if self.drowsy_time is None:
                    self.drowsy_time = time.time()
                elif time.time() - self.drowsy_time >= self.drowsy_trans:
                    self.curr_state = self.state_1
            
            elif cls == 2:
                if self.yawn_time is None:
                    self.yawn_time = time.time()
                elif time.time() -self.yawn_time >= self.yawn_trans:
                    self.curr_state = self.state_2
                  
            else:
                if self.drowsy_time is not None and time.time() - self.drowsy_time >= self.drowsy_trans:
                    self.drowsy_time = None
                
                if self.yawn_time is not None and time.time() - self.yawn_time >= self.yawn_trans:
                    self.yawn_time = None
                
        elif cls == 0:
            self.drowsy_time = None
            self.yawn_time = None
        return self.curr_state

    def drowsy_to_other_states(self, cls):
        if self.curr_state == self.state_1:
            if cls == 0:
                if self.awake_time is None:
                    self.awake_time = time.time()
                elif time.time() - self.awake_time >= self.awake_trans:
                    self.curr_state = self.state_0
            else:
                if self.awake_time is not None and time.time() - self.awake_time >= self.awake_trans:
                    self.awake_time = None                 
        return self.curr_state
    
    def yawn_to_other_states(self, cls):
        if self.curr_state == self.state_2:

            if cls == 0:
                if self.awake_time is None:
                    self.awake_time = time.time()
                elif time.time() - self.awake_time >= self.awake_trans:
                    self.curr_state = self.state_0
                    self.yawn_time = None 
            else:
                self.awake_time = None
        return self.curr_state
    
    def update(self, cls):
        if self.curr_state == self.state_0:
            return self.awake_to_other_states(cls)
        elif self.curr_state == self.state_1:
            return self.drowsy_to_other_states(cls)
        elif self.curr_state == self.state_2:
            return self.yawn_to_other_states(cls) 
        else:
            return self.idle_state

    def outputs(self):
        if self.curr_state == self.state_0:
            label = self.state_0.name
        elif self.curr_state == self.state_1:
            label = self.state_1.name
        elif self.curr_state == self.state_2:
            label = self.state_2.name
        else:
            label = self.idle_state
        return label
