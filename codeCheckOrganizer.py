from codeTestWithTime import CodeCheckSystem
import time
def testCode(code, lessonName):
    timeList = []
    timeSum = 0
    code = code.replace("input(", "inputTest(")

    lessons = {
        #format is lessonName: [code, expectedOutput, input] multiple test cases are stored as seperate tuples
    "1.0": [(code, "Hello World!")],
    "1.1": [(code, "Alex", "Alex"), (code, "Test", "Test"), (code, "12345", "12345")],
    "1.2": [(code, "Hello, Alex", "Alex"), (code, "Hello, John", "John"), (code, "Hello, 1234554321", "1234554321")],

    }

    for lesson in lessons.keys():
        if lesson == lessonName:
            for test in lessons[lesson]:
                try:
                    time1 = time.perf_counter()
                    codeObject = CodeCheckSystem(test[0], test[1], inputFunc=test[2]).basicCheckCode()
                    time2 = time.perf_counter()
                except:
                    time1 = time.perf_counter()
                    codeObject = CodeCheckSystem(test[0], test[1]).basicCheckCode()
                    time2 = time.perf_counter()

                timeTaken = time2 - time1
                
                timeSum += timeTaken

            timeAverage = timeSum / len(lessons[lesson])
    return codeObject, timeAverage
                    

code = """
x = input('What is your name: ')
print('Hello, ' + x)"""
lessonName = "1.2"

print(testCode(code, lessonName))