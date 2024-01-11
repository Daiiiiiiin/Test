from operations.operation import OperationLoop

class MeasurePpcOxy(OperationLoop):
    def __init__(self, start_time, end_time, loop_dt, is_enable, sharedmemory):
        
        super().__init__(start_time, end_time, loop_dt, is_enable, sharedmemory)
        self.operation_name = 'Sensor Ppc Oxy'

        #call sub Thread and start
        self.demon = True
        self.start()  #start하면 뭐가 start 되는건지?

    def initialize(self):
        # operation initialize 랑 다른건데 왜 두 개 필요한지?
        self.test = 1

        print("Initialize")

    def task(self):
        self.run()

    #def terminate(self):