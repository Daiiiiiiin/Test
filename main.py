import sys
sys.dont_write_bytecode =  True

import time
from operations.measure_p_oxy import MeasurePpcOxy
from operations.timer import Timer

class SharedMemory:
    def __init__(self):
        self.runtime = 0
        self.is_running = False

sharedmemory = SharedMemory()

measurement = MeasurePpcOxy(1, 10, 1, True, sharedmemory)
timer = Timer(1, 10, 1, True, sharedmemory)
time.sleep(3)

sharedmemory.is_running = True
timer.task() #TIMER START


#time.sleep(10)