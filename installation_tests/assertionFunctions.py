import config,re,subprocess
from distutils.version import StrictVersion
from os.path import isfile,join
from os.path import sep as pathSeparator
from distutils.version import LooseVersion, StrictVersion



def checkIfPythonModuleIsInstalled(testConfig):
    """
    Checks to see if python module can be loaded successfully
    """
    try:
        exec("import "+testConfig["pyModule"])
        assert True
    except Exception as e:
        assert False, testConfig["name"]+": "+testConfig["pyModule"]+" could not successfully be loaded in Python."


def checkIfServiceIsRunning_Linux(testConfig):
    """
    Greps to see if service is running.  Asserts true if "running" is found, else it fails
    """
    assert "name" in testConfig
    assert "service" in testConfig
    
    command = "sudo service "+testConfig["service"]+" status"
    p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,error = p.communicate()
    
    
    assert re.search("is running",out) ,"\nName :"+testConfig["service"]+\
                        "\nExpected service to be running: "+testConfig["service"]+\
                        "\n Test failed."

def checkIfServiceIsRunning_OSX(testConfig):
    """
    Greps to see if service is running.  Asserts true if "running" is found, else it fails
    """
    assert "name" in testConfig
    assert "service" in testConfig
    
    command = "launchctl list | grep "+testConfig["service"] 
    p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,error = p.communicate()
    
    
    testPass=False
    for output in out:
        if re.match("\d+",output) :
            testPass=True
            break
    
    assert testPass,"\nName :"+testConfig["service"]+\
                        "\nExpected service to be running: "+testConfig["service"]+\
                        "\n Test failed."





def checkIfFileExistsInPossibleLocations(testConfig):
    """
    Checks if testConfig["file"] exists in the directories testConfig["file_locations"]
    """
    assert "name" in testConfig
    assert "file" in testConfig
    assert "file_locations" in testConfig
    testPass = False
    for filePath in testConfig["file_locations"]:
        if isfile(join(filePath,testConfig["file"])):
            testPass=True
    
    assert testPass,"Failure for package "+testConfig["name"]+"\n File: "+\
                        testConfig["file"]+" does not exist"+"\nSearched in "+\
                        str(testConfig["file_locations"])
    
def checkIfFileExists(testConfig):
    """
    Checks if testConfig["file"] exists on the system
    """
    assert "name" in testConfig
    assert "file" in testConfig
    if type(testConfig["file"]) != list:
	    testConfig["file"] = [testConfig["file"]]
    for file in testConfig["file"]:
	    assert isfile(file), "Failure for package "+testConfig["name"]+"\n File: "\
           +file+" does not exist"

def checkIfMinimumVersionIsMet(testConfig):
    """
    Runs testConfig["version_command"] (If not set, default is 'testConfig["name"] --version')
    Pulls out anything possible strings that could be version strings
    If any of those strings are a higher version than testConfig["minimum_version"], then we assert True
    """
    assert "name" in testConfig
    assert "binary" in testConfig
    assert "minimum_version" in testConfig
    
    #Set default version command as "testConfig["name"] --version"
    #Otherwise, use testConfig["version_command"]
    if "version_command" in testConfig:
        versionCommand = testConfig["version_command"]
    else:
        versionCommand = testConfig["binary"]+r" --version"
    
    #Run the version command, grab stdout and stderr
    p = subprocess.Popen(versionCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    versionOut,versionError = p.communicate()
    versionOut = str(versionOut)+str(versionError)
    
    #Find all instances of something that could be the version number in the output
    installedVersion = re.findall(r"([0-9]+\.)+[0-9]+", versionOut)
    
    #Go through all the matches, if anything starts with our expected version,
    #Set test as pass
    testPass=False
    for version in installedVersion:
        if LooseVersion(str(version)) >= LooseVersion(testConfig["minimum_version"]):
            testPass=True
            break
    
    assert testPass,"\nVersion output was :"+versionOut+\
                        "\nExpected minimum version: "+testConfig["minimum_version"]+\
                        "\n Test failed."


def checkIfVersionIsExact(testConfig):
    """
    Runs testConfig["version_command"] (If not set, default is 'testConfig["name"] --version')
    Pulls out anything possible strings that could be version strings
    If any of those strings start with the expcted version from testConfig["version"], then we assert True
    """
    assert "name" in testConfig
    assert "binary" in testConfig
    assert "version" in testConfig
    
    #Set default version command as "testConfig["name"] --version"
    #Otherwise, use testConfig["version_command"]
    if "version_command" in testConfig:
        versionCommand = testConfig["version_command"]
    else:
        versionCommand = testConfig["binary"]+r" --version"
    
    #Run the version command, grab stdout and stderr
    p = subprocess.Popen(versionCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    versionOut,versionError = p.communicate()
    versionOut = str(versionOut)+str(versionError)
    
    #Find all instances of something that could be the version number in the output
    installedVersion = re.findall(r"([0-9.]*[0-9]+)", versionOut)
    
    #Go through all the matches, if anything starts with our expected version,
    #Set test as pass
    testPass=False
    for version in installedVersion:
        if re.match(testConfig["version"],str(version)) :
            testPass=True
            break
    
    
    assert testPass,"\nVersion output was :"+versionOut+\
                        "\nExpected version: "+testConfig["version"]+\
                        "\n Test failed."
    
    

def checkIfWhichCanFindBinary(testConfig):
    """
    Runs "which" command against testConfig["name"]
    if which has return code == 0 then pass.  Else, fail
    """
    assert "name" in testConfig
    cmd = ["which",testConfig["binary"] ]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    res = p.communicate()
    assert  str(p.returncode) == str(0), "\"which\" command failed to return anything for "+testConfig["name"]+": "+testConfig["binary"]+" :Test failed."
    
