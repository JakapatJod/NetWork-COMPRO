from threading import Thread

class myTread(Thread):
    def __init__(self,name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        print('Hello, my name is %s\n'%self.getName())
    
process1 = myTread('Thread 1')
process2 = myTread('Thread 2')
process3 = myTread('Thread 3')

process1.start()
process2.start()
process3.start()