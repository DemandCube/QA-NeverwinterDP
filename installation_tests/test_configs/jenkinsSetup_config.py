import site


check_config = [
    {
        "name":"git",
        "binary":"git",
        "minimum_version":"1.8"
    },
    {
        "name":"nosetests",
        "binary":"nosetests",
        
    },
    {
        "name":"python",
        "binary":"python",
        #Python will usually say its version 2.7.x
        #This works because we only try to re.match (not re.search)
        #the version number
        "version":"2.6.6",
        #This version_command is actually not necessary
        #since the default behavior is to run '[binary] --version"
        #Putting it here just as an example for now
        "version_command":"python --version"
    },
    {
        "name":"easy_install",
        "binary":"easy_install",
    },
    {
        "name":"pip",
        "binary":"pip",
    },
    {
        "name":"java",
        "binary":"java",
    },
    {
        "name":"jenkins",
        "service":"jenkins",
    },
    
]