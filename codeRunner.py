import builtins
from RestrictedPython import compile_restricted
from RestrictedPython import utility_builtins
import time

error = False

def limited_range(iFirst, *args):
    # limited range function from Martijn Pieters
    RANGELIMIT = 1000
    if not len(args):
        iStart, iEnd, iStep = 0, iFirst, 1
    elif len(args) == 1:
        iStart, iEnd, iStep = iFirst, args[0], 1
    elif len(args) == 2:
        iStart, iEnd, iStep = iFirst, args[0], args[1]
    else:
        raise AttributeError('range() requires 1-3 int arguments')
    if iStep == 0:
        raise ValueError('zero step for range()')
    iLen = int((iEnd - iStart) / iStep)
    if iLen < 0:
        iLen = 0
    if iLen >= RANGELIMIT:
        raise ValueError(
            'To be created range() object would be to large, '
            'in our IDE we only allow {limit} '
            'elements in a range.'.format(limit=str(RANGELIMIT)),
        )
    return range(iStart, iEnd, iStep)


class PrintCollector(object):
    """Collect written text, and return it when called."""

    def __init__(self, _getattr_=None):
        self.txt = []
        self._getattr_ = _getattr_

    def write(self, text):
        self.txt.append(text)

    def __call__(self):
        return ''.join(self.txt)

    def _call_print(self, *objects, **kwargs):
        if kwargs.get('file', None) is None:
            kwargs['file'] = self
        else:
            self._getattr_(kwargs['file'], 'write')

        print(*objects, **kwargs)
        printList.append(objects)
        sendString(*objects, False)


#a fuction that sends the string to the frontend using django to be displayed in realtime without a url change
def sendString(string, error):
    pass
    
    
def input(string):
    PrintCollector(string)
    answer = getInput()
    return answer

def getInput():
    string = ""
    #gets input from frontend with django without a url change
    return string

restricted_globals = dict(__builtins__=utility_builtins)

MAX_ITER_LEN = 100

class MaxCountIter:
    def __init__(self, dataset, max_count):
        self.i = iter(dataset)
        self.left = max_count

    def __iter__(self):
        return self

    def __next__(self):
        if self.left > 0:
            self.left -= 1
            return next(self.i)
        else:
            raise StopIteration()

def _getiter(ob):
    return MaxCountIter(ob, MAX_ITER_LEN)


def inputTest(string):
    return inputTestValue


def compileRun(userInput, inputTestValue=""):
    printList = []
    __builtins__['printList'] = printList
    __builtins__['inputTestValue'] = inputTestValue
    restricted_globals.update({
    "_getiter_": _getiter,
    '_print_': PrintCollector,
    "_getattr_": getattr,
    "range": limited_range,
    "input": input,
    "inputTest": inputTest,
    })

    printList = __builtins__['printList']

    error = False
    try:
        byte_code = compile_restricted(userInput, '<string>', 'exec')
        tic = time.perf_counter()
        exec(byte_code, restricted_globals)
        toc = time.perf_counter()
        timeTaken = toc - tic

    except SyntaxError as e:
        printList.append(e)
        sendString(e, True)
        error = True

    except ImportError:
        printList.append("You are trying to import a module that isn't allowed")
        sendString("You are trying to import a module that isn't allowed", True)
        error = True

    except NameError as e:
        printList.append(e)
        sendString(e, True)
        printList.append("You may not be using a function you're allowed to")
        sendString("You may not be using a function you're allowed to", True)
        error = True
    #print(__builtins__['printList'])
    return printList, timeTaken