import sys
import os

def prepSysPathForTests():
    pathToFunctionModule = os.getcwd()
    sys.path.append(pathToFunctionModule)