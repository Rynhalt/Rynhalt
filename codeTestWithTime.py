import numpy
import time
from io import StringIO  
import sys
import codeRunner

import warnings
warnings.filterwarnings("ignore")

x = """
def add_slow(a, b):
    return a+b
print("a")  
print("b")
x = 3
y = 7
input("Press Enter to continue...")
print(x+y)
"""

def listToString(s):  
    str1 = ""  
    for ele in s:
        print(ele)  
        str1 += (str(ele[0]) + "\n")
    return str1

class CodeCheckSystem():
    def __init__(self,codeToCheck, expectedOuput, inputFunc=None):
        self.code = codeToCheck
        self.expOutput = expectedOuput
        self.result_list = []
        self.inputFunc = inputFunc

    def run(self):
        timetook = 0
        # calculated the time it takes to run the code
        start_time = time.time()
        self.result_list, timeTaken = codeRunner.compileRun(self.code, inputTestValue=self.inputFunc)
        self.timetook = time.time() - start_time
        

    def basicCheckCode(self):
        # Then, get the stdout like a string and process it!
        self.run()
        result_string = listToString(self.result_list)
        print(result_string)
        
        if self.isCorrect(result_string):
            print("Correct")
            return True
        else:
            print("Incorrect")
            return False

    def basicCheckCodeWithFunction(self, functionName, input, returnCheck):
        self.run()
        if input != None:
            tic = time.perf_counter()
            result = codeRunner.restricted_globals[functionName](*input)
            toc = time.perf_counter()
        else:
            tic = time.perf_counter()
            result = codeRunner.restricted_globals[functionName]()
            toc = time.perf_counter()
        timeTaken = toc - tic

        if returnCheck:
            if result == self.expOutput:
                print("Correct")
                return True, timeTaken
            else:
                print("Incorrect")
                return False, timeTaken
        
        else:
            result_string = listToString(self.result_list)
            print(result_string)
        
            if self.isCorrect(result_string):
                print("Correct")
                return True, timeTaken
            else:
                print("Incorrect")
                return False, timeTaken
    
    def isCorrect(self, result):
        if str(self.expOutput) + "\n" == result:
            return True
        else:
            return False


#CodeCheckSystem(x, 10).basicCheckCode()
#CodeCheckSystem(x, 6, inputToCheck=(2, 4)).basicCheckCodeWithFunction("add_slow", True, True)