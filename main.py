import sys
sys.dont_write_bytecode =  True

import time
from operations.measure_p_oxy import MeasurePpcOxy

class SharedMemory:
    def __init__(self):
        self.runtime = 0
        self.is_running = False

sharedmemory = SharedMemory()

measurement = MeasurePpcOxy(1, 5, 0.1, True, sharedmemory)
#measurement = operations.MeasurePpcOxy(0, 10, 0.1, True, sharedmemory)
#여기서 is_enable이 True되면서 operationLoop 의 run(초기화) 작동

time.sleep(1)

sharedmemory.is_running = True
#task 작동 하도록

time.sleep(5)