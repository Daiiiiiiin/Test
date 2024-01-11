from .operation import OperationLoop

class MeasurePpcCH4(OperationLoop):
    def __init__(self, start_time, end_time, loop_dt, is_enable, sharedmemory):
        
        super().__init__(start_time, end_time, loop_dt, is_enable, sharedmemory)
        self.operation_name = 'Sensor Ppc CH4'

        #call sub Thread and start
        self.demon = True
        self.start()

    def initialize(self):
        self.test = 1

        print("Initialize")

    def task(self):
        print(self.test)

    def terminate(self):
        pass