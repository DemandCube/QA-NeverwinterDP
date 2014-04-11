import config,assertionFunctions,sys,imp
from os import path

ROLES_PKG_NAME = "roles"
ROLES_DIR = path.join(path.dirname(path.realpath(__file__)), ROLES_PKG_NAME)

def dynamicallyLoadModule(name):
    """
    Helper function. Loads a module dynamically from the ROLES_PKG_DIR location
    @param name: The name of the module to load from roles
    @return: The module that has been loaded
    """
    f, file, desc=imp.find_module(name, [ROLES_DIR])
    return imp.load_module(ROLES_PKG_NAME+'.'+name, f, file, desc)

def test_ifWhichCanFindBinary():
    """
    Runs through testConfig.  Anything with a roles.(name).config["binary"] will be run against the "which" command
    to see if a binary is in place
    Test generator
    """
    for name in config.toTest:
        testConfig = dynamicallyLoadModule(name)
        if "binary" in testConfig.config:
            print "Binary: "+ testConfig.config["name"]
            yield assertionFunctions.checkIfWhichCanFindBinary, testConfig.config
            
def test_ifPythonModuleIsInstalled():
    """
    Runs through testConfig.  Anything with a roles.(name).config["pyModule"] will be attempted to be loaded in Python.
    If it can be loaded the test passes, otherwise fail
    Test generator
    """
    for name in config.toTest:
        testConfig = dynamicallyLoadModule(name)
        if "pyModule" in testConfig.config:
            print "pyModule: "+ testConfig.config["name"]
            yield assertionFunctions.checkIfPythonModuleIsInstalled, testConfig.config
            


def test_ifServicesAreRunning():
    """
    Runs through testConfig.  Anything with a roles.(name).config["service"] will be tested to see if the service is running
    Test generator
    """
    for name in config.toTest:
        testConfig = dynamicallyLoadModule(name)
        if "service" in testConfig.config:
            print "Service: "+ testConfig.config["name"]
            if sys.platform.startswith("darwin"):
                yield assertionFunctions.checkIfServiceIsRunning_OSX, testConfig.config
            elif sys.platform.startswith("linux"):
                yield assertionFunctions.checkIfServiceIsRunning_Linux, testConfig.config
            else:
                assert False, str(sys.platform)+": Not supported!"


def test_ifVersionIsCorrect():
    """
    Runs through testConfig.  Anything with a roles.(name).config["version"] will be run
    against the roles.(name).config["version_command"] command to see if the minimum version is met
    If no roles.(name).config["version_command"] is set, "roles.(name).config["binary"] --version" is the default string used
    Test generator
    """
    
    for name in config.toTest:
        testConfig = dynamicallyLoadModule(name)
        if "version" in testConfig.config:
            print "Version: "+ testConfig.config["name"]
            yield assertionFunctions.checkIfVersionIsExact, testConfig.config
            
        if "minimum_version" in testConfig.config:
            print "Minimum Version: "+ testConfig.config["name"]
            yield assertionFunctions.checkIfMinimumVersionIsMet, testConfig.config

def test_ifFileExists():
    """
    Runs through test Config.  Anything with roles.(name).config["file"] will be tested
    """
    for name in config.toTest:
        testConfig = dynamicallyLoadModule(name)
        if "file" in testConfig.config and "file_locations" in testConfig.config:
            print "File In Location: "+ testConfig.config["name"]
            yield assertionFunctions.checkIfFileExistsInPossibleLocations, testConfig.config
        elif "file" in testConfig.config:
            print "File: "+ testConfig.config["name"]
            yield assertionFunctions.checkIfFileExists, testConfig.config

