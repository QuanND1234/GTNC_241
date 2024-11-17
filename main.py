from ThreadTimeout import func_timeout, FunctionTimedOut, func_set_timeout
import time
class Solution:
    def __init__(self):
        pass
    def timeout_child(self):
        time.sleep(0.001)
    def timeout_handler(self,s:str):
        time.sleep(0.06)
        self.timeout_child()
        return 'result'
    def process(self):
        try:
            res = func_timeout(0.06, self.timeout_handler,args=('nam',))
            res = self.timeout_handler()
            return res
        except FunctionTimedOut:
            print('timeout 0.1s')
            return 'default'

        # Thiết lập timeout 0.1 giây
if __name__ == "__main__":
    solution = Solution()
    for i in range(10):
        start = time.perf_counter_ns()
        answer = solution.process()
        end = time.perf_counter_ns()
        print('max_time', (end - start) / 1_000_000_000)
        print('answer',answer)
