import time
from  .operation import OperationLoop

class MeasurePpcOxy(OperationLoop):
    def __init__(self, start_time, end_time, loop_dt, is_enable, sharedmemory):
        
        super().__init__(start_time, end_time, loop_dt, is_enable, sharedmemory)
        self.operation_name = 'MeasurePpcOxy'
        

        self.demon = True
        self.start() 
        # 이 class 선언하자마자 부모 class(Operation Loop)의 run함수 실행됨

        print("Initialize")

    def run_task(self): 
        
        print("i'm Measure Ppc Oxy task")
        time.sleep(5)
        

    def terminate(self):

        for i in range(4):
            print("i'm Measure Ppc Oxy terminate")
        return NotImplementedError