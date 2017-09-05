from threading import Thread,Event
from os import (listdir, remove, system, path)
import time

TIMER_TIME = 10 # seconds to print files
PATH_TO_FOLDER = 'E:\\test\\' # path to print folder
C_FILES = 5 # count of files in folder to print


FILES = []

def printFiles(): # func to prepare files to print
	if FILES != []: # if files in folder
		for file in FILES:
			try:
				remove(PATH_TO_FOLDER + file.replace('\\', ''))
			except FileNotFoundError as err:
				pass

class MyTimer:
    def __init__(self, mytime, function):
        self.mytime=mytime
        self.function=function
        self.start=time.time()
        self.event= Event()
        self.thread=Thread(target=self._target)
        self.thread.start()
    def _target(self):
        while not self.event.wait(self._time):
            self.function()
    @property
    def _time(self):
        return self.mytime-((time.time()-self.start)%self.mytime)

    def stop(self):
        self.event.set()
        self.thread.join()


def removeFiles():
	printFiles()
	print(FILES)

if __name__ == '__main__':
    timer=MyTimer(10, removeFiles)
    while True:
        FILES = listdir(PATH_TO_FOLDER)
        time.sleep(1)
        if len(FILES) >= C_FILES:
            removeFiles()
            timer.stop()
            timer=MyTimer(10, removeFiles)
