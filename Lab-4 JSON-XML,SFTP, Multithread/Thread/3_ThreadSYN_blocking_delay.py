from threading import Thread
import threading
import time

# การทำงานต้องรอ thread 1 ทำเสร็จก่อนค่อยทำ thread 2 มีสถานะ waiting

class myThread(Thread):
    def __init__(self,threadID,name,counter):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    
    def printTime(self,threadName, delay, counter):
        while counter:
            time.sleep(delay)
            print('%s: %s' %(threadName,time.ctime(time.time())))
            counter -= 1
    def run(self):  # Overriding run method
        print('Starring ' + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()           # การทำ blocking ควรมี .acquire() และ .release()
    
        self.printTime(self.name , self.counter,3)
        # Free lock to release next thread
        threadLock.release()

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = myThread(1,"Thread - 1",1)
thread2 = myThread(2,"Thread - 2",2)

# Start new Threads
thread1.start()
thread2.start()

# append threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
