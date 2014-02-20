import site


check_config = [
    {
        "name":"git",
        "binary":"git",
        "minimum_version":"1.7"
    },
    {
        "name":"nosetests",
        "binary":"nosetests",
        
    },
    {
        "name":"python",
        "binary":"python",
        "version":"2.7",
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
        "name":"ansible",
        "binary":"ansible",
    },
    {
        "name":"virtualbox",
        "binary":"virtualbox",
    },
    {
        "name":"vagrant",
        "binary":"vagrant",
    },
    {
        "name":"java",
        "binary":"java",
    },
    {
        "name":"pyYaml",
        "file":r"yaml/__init__.py",
        "file_locations": site.getsitepackages()
    },
    {
        "name":"paramiko",
        "file":r"paramiko/__init__.py",
        "file_locations": site.getsitepackages()
    },
    {
        "name":"jinja2",
        "file":r"jinja2/__init__.py",
        "file_locations": site.getsitepackages()
    },
    {
        "name":"httplib2",
        "file":r"httplib2/__init__.py",
        "file_locations": site.getsitepackages()
    },
    {
        "name":"python ansible",
        "file":r"ansible/__init__.py",
        "file_locations": site.getsitepackages()
    },
    
]