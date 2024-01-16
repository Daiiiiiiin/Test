import time
from operations.operation import OperationLoop

class Timer(OperationLoop):

    def __init__(self, start_time, end_time, loop_dt, is_enabl, sharedmemory):
        
        super().__init__(start_time, end_time, loop_dt, is_enabl, sharedmemory)
        self.operation_name = 'Timer'

        #수정
        self.mission_time = 10

        self.demon = True
        self.start() 

    def task(self): #TIMER START

        while not self.sharedmemory.is_running: time.sleep(1e-9)

        starttime = time.time()

        ###end time -> mission time으로 바꿔야함
        while self.sharedmemory.is_running and self.sharedmemory.runtime < self.end_time:
            
            self.sharedmemory.runtime = time.time() - starttime
            
            print('current tuntime: {}'.format(self.sharedmemory.runtime))

            ###time 0.5 -> 1e-9
            time.sleep(0.5)

        self.sharedmemory.is_running = False

        time.sleep(0.5)
        
        # print("="*80)
        # #NRM, BLD 있음
        # print("{:^80}".format("Experiment Done"))
        # print("{:^80}".format("Press 'Enter' to exit"))
        # print("="*80)

    #test for OpertaionLoop run function
    def run_task(self):
        print('timer_run_time: test for OperationLoop run function')
  


