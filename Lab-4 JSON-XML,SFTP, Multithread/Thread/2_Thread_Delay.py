from threading import Thread
import time


class myTread(Thread): # Extending Thread class
    def __init__(self,threadID,name,counter):
        Thread.__init__(self)  # Overriding __init__ method
        self.name = name
        self.threadID = threadID
        self.counter = counter

    def printTime(self, threadName , delay , counter):
        while counter:
            time.sleep(delay)
            print("%s: %s"%(threadName,time.ctime(time.time())))
            counter -= 1
     
    def run(self):  # Overriding run method
        print('Starring ' + self.name)
        self.printTime(self.name , self.counter,5)
        print('Exiting' + self.name)
    
# Create new threads
thread1 = myTread(1,'Thread-1',1)
thread2 = myTread(2,'Thread-2',2)

# Start new thread
thread1.start()
thread2.start()

