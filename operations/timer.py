import time
from operations.operation import OperationLoop

class Timer(OperationLoop): #애는 mission time 받아옴

    def __init__(self, start_time, end_time, loop_dt, is_enabl, sharedmemory):
        
        super().__init__(start_time, end_time, loop_dt, is_enabl, sharedmemory)
        self.operation_name = 'Timer'
        #수정
        self.mission_time = 10

        self.demon = True
        self.start() 

    def timer_start(self): #Timer는 is_running = True 되자마자 바로 시작해야하니 메인으로 따로 뻄.

        while not self.sharedmemory.is_running: time.sleep(1e-9)

        starttime = time.time()
        self.sharedmemory.runtime = 0
        
        ###end time -> mission time으로 바꿔야함
        while self.sharedmemory.is_running and self.sharedmemory.runtime < self.end_time:
            
            self.sharedmemory.runtime = time.time() - starttime
            
            print('current tuntime: {}'.format(self.sharedmemory.runtime))

            ###수정 time 0.5 -> 1e-9
            time.sleep(0.5)

        self.sharedmemory.is_running = False

        time.sleep(0.5)
        
        print("="*80)
        #print(BLD+"{:^80}".format("Experiment Done")+NRM)
        print("{:^80}".format("Press 'Enter' to exit"))
        print("="*80)

    def run_task(self):
        pass
  


