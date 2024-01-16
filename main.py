import sys
sys.dont_write_bytecode =  True

import time
import operations

class SharedMemory:
    def __init__(self):
        self.runtime = 0
        self.is_running = False

sharedmemory = SharedMemory()

measurement = operations.MeasurePpcOxy(1, 10, 1, True, sharedmemory)
timer = operations.Timer(1, 10, 1, True, sharedmemory)
time.sleep(3)

sharedmemory.is_running = True
timer.task() #TIMER START


#time.sleep(10)