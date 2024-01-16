from operations.operation import OperationLoop

class MeasurePpcOxy(OperationLoop):
    def __init__(self, start_time, end_time, loop_dt, is_enable, sharedmemory):
        
        super().__init__(start_time, end_time, loop_dt, is_enable, sharedmemory)
        self.operation_name = 'MeasurePpcOxy'
        

        self.demon = True
        self.start() 
        # 이 class 선언하자마자 run함수 실행됨 (부모)

        self.test = 1

        print("Initialize")

    def run_task(self): 
        
        #for i in range(2):
        print("i'm Measure Ppc Oxy task")

        return NotImplementedError

    def terminate(self):

        for i in range(4):
            print("i'm Measure Ppc Oxy terminate")


        return NotImplementedError