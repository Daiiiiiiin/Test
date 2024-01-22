import sys
sys.dont_write_bytecode =  True

import time
import operations

class SharedMemory:
    def __init__(self):
        self.runtime = 0
        self.is_running = False

sharedmemory = SharedMemory()

measurement = operations.MeasurePpcOxy(3, 10, 1, True, sharedmemory)
timer = operations.Timer(1, 10, 1, True, sharedmemory)

sharedmemory.is_running = True
timer.timer_start() #얘만 먼저 시작하게 따로 빼줌

#time.sleep(10)