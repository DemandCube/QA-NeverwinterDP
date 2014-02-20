import config,assertionFunctions
import sys



def test_ifServicesAreRunning():
    """
    Runs through testConfig.  Anything with a testConfig["service"] will be tested to see if the service is running
    Test generator
    """
    for testConfig in config.check_config:
        
        if "service" in testConfig:
            if sys.platform.startswith("darwin"):
                yield assertionFunctions.checkIfServiceIsRunning_OSX, testConfig
            elif sys.platform.startswith("linux"):
                yield assertionFunctions.checkIfServiceIsRunning_Linux, testConfig
            else:
                assert False, str(sys.platform)+": Not supported!"
    

def test_ifWhichCanFindBinary():
    """
    Runs through testConfig.  Anything with a testConfig["binary"] will be run against the "which" command
    to see if a binary is in place
    Test generator
    """
    for testConfig in config.check_config:
        if "binary" in testConfig:
            yield assertionFunctions.checkIfWhichCanFindBinary, testConfig
    
def test_ifVersionIsCorrect():
    """
    Runs through testConfig.  Anything with a "version" will be run
    against the testConfig["version_command"] command to see if the minimum version is met
    If no testConfig["version_command"] is set, "testConfig["binary"] --version" is the default string used
    Test generator
    """
    for testConfig in config.check_config:
        if "version" in testConfig:
            yield assertionFunctions.checkIfVersionIsExact, testConfig
            
        if "minimum_version" in testConfig:
            yield assertionFunctions.checkIfMinimumVersionIsMet, testConfig

def test_ifFileExists():
    """
    Runs through test Config.  Anything with "file" will be run
    """
    for testConfig in config.check_config:
        if "file" in testConfig and "file_locations" in testConfig:
            yield assertionFunctions.checkIfFileExistsInPossibleLocations, testConfig
        elif "file" in testConfig:
            yield assertionFunctions.checkIfFileExists, testConfig

