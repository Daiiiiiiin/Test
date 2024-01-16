import time
import sys
from threading import Thread

class OperationLoop(Thread):
    def __init__(self, start_time, end_time, loop_dt, is_enable, sharedmemory):
        
        super().__init__()
        self.start_time     = start_time
        self.end_time       = end_time
        self.loop_dt        = loop_dt
        self.is_enable      = is_enable
        self.sharedmemory   = sharedmemory
        self.operation_name = None

    def initialize(self):
 
        print("operationLoop.initialize")
        return NotImplementedError
    
    def task(self):
        
        print("operationLoop task are working")
        return NotImplementedError
    
    def terminate(self):
        sys.exit()
    
    def run(self):

        if self.is_enable:

            self.initialize()

            print("{:<50}".format(self.operation_name + " ") + "{:>20}".format(" Initialized") + " at {:>5}s".format(self.sharedmemory.runtime))

            while not self.sharedmemory.is_running: time.sleep(1e-6)

            while self.sharedmemory.is_running and self.sharedmemory.runtime < self.start_time: time.sleep(1e-6)

            print("{:<50}".format(self.operation_name + " ") + "{:>20}".format(" Started") + " at {:>5}s".format(self.sharedmemory.runtime))

            while self.sharedmemory.is_running and self.sharedmemory.runtime < self.end_time:   
                
                self.run_task()
                ### 여기서 자식 클래스의 run_task 함수 호출하면 실행됨 (여기 있는 함수랑 자식 클래스 함수랑 이름 같으면 자식 클래스 함수 우선 호출)
                ### 현재는 measure_p_oxy.py 와 timer 의 run_task() 동시 실행
                time.sleep(self.loop_dt)

            print("{:<50}".format(self.operation_name + " ") + "{:>20}".format(" Done") + " at {:>5}s".format(self.sharedmemory.runtime))

            self.terminate()


class OperationOnce(Thread):

    def __init__(self, start_time, loop_dt, is_enable, sharedmemory):
        
        super().__init__()
        self.start_time     = start_time
        self.loop_dt        = loop_dt
        self.is_enable      = is_enable
        self.sharedmemory   = sharedmemory
        self.operation_name = None

    def initialize(self):
        raise NotImplementedError
    
    def task(self):
        raise NotImplementedError
    
    def terminate(self):
        raise NotImplementedError
    
    def run(self):

        if self.is_enable:
            self.initialize()
            
            print("{:<50}".format(self.operation_name + " ") + "{:>20}".format(" Initialized") + " at {:>5}s".format(self.sharedmemory.runtime))
            
            while not self.sharedmemory.is_running: time.sleep(1e-6)

            while self.sharedmemory.is_running and self.sharedmemory.runtime < self.start_time: time.sleep(1e-6)

            print("{:<50}".format(self.operation_name + " ") + "{:>20}".format(" Started") + " at {:>5}s".format(self.sharedmemory.runtime))

            self.task()
            
            print("{:<50}".format(self.operation_name + " ") + "{:>20}".format(" Done") + " at {:>5}s".format(self.sharedmemory.runtime))

            self.terminate()