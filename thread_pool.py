#!/usr/bin/env python3
# encoding: utf-8

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import queue
import threading
import log

class worker(threading.Thread):
    worker_count = 0
    
    def __init__(self, work_queue, result_queue, timeout=0, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.id = worker.worker_count
        worker.worker_count += 1
        self.daemon = True
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.timeout = timeout

    def run(self):
        ''' the get-and-do loop'''
        while True:
            try:
                callable, args, kwargs = self.work_queue.get(timeout=self.timeout)
                result = callable(*args, **kwargs)
                if result: self.result_queue.put(result) # only add url_graph result, filter indexing result
                # print('worker[%d]: %s' % (self.id, str(result)))
                # no task_done() means can't be join() now,run the next cycle
            except queue.Empty:
                break
            except:
                import sys
                log.log_traceback()
                print('worker[%d]' % self.id, sys.exc_info()[:2])

class thread_pool(object):
    def __init__(self, num_workers=10, timeout=1):
        self.work_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads(num_workers)

    def _recruitThreads(self, num_workers):
        for i in range(num_workers):
            worker_obj = worker(self.work_queue, self.result_queue, self.timeout)
            self.workers.append(worker_obj)

    def start(self):
        for w in self.workers:
            w.start()

    def wait_completion(self):
        # waiting for each worker to terminate
        while len(self.workers):
            worker_obj = self.workers.pop()
            worker_obj.join() # blocking, waiting for the all complete.
            if worker_obj.is_alive() and not self.work_queue.Empty:
                self.workers.append(worker_obj)

    def add_job(self, callable, *args, **kwargs):
        self.work_queue.put( (callable, args, kwargs) )

    def get_one_result(self, *args, **kwargs):
        if not self.result_queue.empty():
            return self.result_queue.get(*args, **kwargs)
        return None

if __name__ == '__main__':
    import md5
    obj = thread_pool(3)
    for i in range(10):
        obj.add_job(md5.md5_str, 'who are you')
    obj.start()
    for i in range(10):
        obj.add_job(md5.md5_str, 'where are we')
    obj.wait_completion()
    ret = obj.get_one_result()
    while ret:
        print(ret)
        ret = obj.get_one_result()
