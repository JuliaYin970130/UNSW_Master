import doctest
import os 

def testAssign(path):
    '''
    >>> testAssign('input1.txt')
    wall1:5
    wall2:0
    wall3:0
    wall4:0
    roof:99
    cost:161
    >>> testAssign('input2.txt')
    wall1:5
    wall2:10
    wall3:34
    wall4:0
    roof:46
    cost:157
    >>> testAssign('input3.txt')
    wall1:5
    wall2:32
    wall3:34
    wall4:5
    roof:47
    cost:185
    >>> testAssign('input4.txt')
    foundation:0
    wall1:24
    wall2:9
    wall3:9
    wall4:11
    roof:21
    painting:40
    cost:194
    >>> testAssign('input5.txt')
    No solution
    >>> testAssign('input6.txt')
    No solution
    '''
    command = "python3 temporalPlanner.py "+path
    print(os.popen(command).read())
if __name__ == "__main__":
    doctest.testmod(verbose=True)
