import os
from os.path import expanduser
import subprocess
from installation_tests import assertionFunctions
from vagrant_image_tests import config

__author__ = 'hikmat'

"""
asserts against result code passed as parameter
and results to success if return code is 0 and
otherwise test is marked as failed with return code non-zero

"""

def assert_success(return_code, v_cmd):
    # if command was executed successfully then result is 0
    assert str(return_code) == str(0), "\n>>>>>>>>>Return Code: %s" % return_code + "\n>>>>>>>>>Test failed!!! for command" + " " + v_cmd


"""
Tests following vagrant commands against vagrant image being tested.
Commands being tested are:
1. vagrant box add box_name box_url
2. mkdir $HOME/test_project_dir && cd test_project_dir
2. vagrant init box_name
3. vagrant up
4. vagrant ssh, vagrant ssh and execute commands, vagrant ssh and verify installed packages
5. vagrant halt
6. vagrant destroy
7. vagrant remove

"""

def test_image_installation():
    # test whether prerequisites are available on system or not
    for testConfig in config.check_config:
        if testConfig["box_url"] != "":
            if "prerequisites" in testConfig:
                    for innerTestConfig in testConfig["prerequisites"]:
                        if "binary" in innerTestConfig:
                            yield assertionFunctions.checkIfWhichCanFindBinary, innerTestConfig

            # start command (vagrant add) execution process, then wait
            v_box = subprocess.Popen(["vagrant", "box", "add", testConfig["box_name"], testConfig["box_url"]])
            # now wait for command execution completion
            v_box.communicate()
            # assert that command executed successfully
            assert_success(v_box.returncode, "vagrant box add")

            # create a directory for vagrant project home
            v_dir = expanduser("~")+"/test_project_dir"
            if not os.path.exists(v_dir):
                os.makedirs(v_dir)
                os.chdir(v_dir)
            else:
                exit(">>>>>>> " + v_dir + " already exists.Please remove it before running")

            # start command (vagrant init) execution process, then wait
            v_init = subprocess.Popen(["vagrant", "init", testConfig["box_name"]])
            # now wait for command execution completion
            v_init.communicate()
            # assert that command executed successfully
            assert_success(v_init.returncode, "vagrant init")

            # start command (vagrant up ) execution process, then wait
            v_up = subprocess.Popen(["vagrant", "up"])
            # now wait for command execution completion
            v_up.communicate()
            # assert that command executed successfully
            assert_success(v_up.returncode, "vagrant up")

            # verify that vagrant user has sudo access
            # First switch to root user and then execute the command passed as -s option
            v_up = subprocess.Popen(["vagrant", "ssh", "-c", "sudo -s exit"])
            # now wait for command execution completion
            v_up.communicate()
            # assert that command executed successfully
            assert_success(v_up.returncode, "vagrant ssh -c sudo -s exit")

            # creates a file inside /vagrant directory of installed box to verify that box allows file creation
            v_ssh = subprocess.Popen(["vagrant", "ssh", "-c", "echo Hello from vagrant > /vagrant/Testfile.txt"])
            # now wait for command execution completion
            v_ssh.communicate()
            # assert that command executed successfully
            assert_success(v_ssh.returncode, "vagrant ssh")

            # verify that file created in shared folder by guest system is accessible in host system
            guest_file = subprocess.Popen(["cat", v_dir + "/Testfile.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            guest_file_content, guest_file_err = guest_file.communicate()
            assert str(guest_file_content.strip()) == str("Hello from vagrant".strip()), "Error while accessing shared file"

            # create a file in host system
            v_local = subprocess.Popen(["echo Hello from host >" + v_dir + "/Testfile1.txt"], shell=True)
            v_local.communicate()
            assert_success(v_local.returncode, "Testfile1.txt")

            # verify that file created in shared folder by host system is accessible in guest system
            host_file = subprocess.Popen(["vagrant", "ssh", "-c", "cat /vagrant/Testfile1.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            host_file_content, host_file_err = host_file.communicate()
            assert str(host_file_content.strip()) == str("Hello from host".strip()), "Error while accessing host file"
            

            # test whether the packages specified in packages section config file
            # are installed in vagrant box or not
            if "packages" in testConfig:
                for packageTestConfig in testConfig["packages"]:
                    if "binary" in packageTestConfig:
                        assert "name" in packageTestConfig
                        # Run command inside of vagrant box
                        v_ssh_cmd = subprocess.Popen(["vagrant", "ssh", "-c", "which" + " " + packageTestConfig["binary"]])
                        # now wait for command execution completion
                        v_ssh_cmd.communicate()
                        # assert command execution
                        assert_success(v_ssh_cmd.returncode, "vagrant ssh -c which" + " " + packageTestConfig["binary"])

            # start command (vagrant halt ) execution process, then wait
            v_halt = subprocess.Popen(["vagrant", "halt"])
            # now wait for command execution completion
            v_halt.communicate()
            # assert that command executed successfully
            assert_success(v_halt.returncode, "vagrant halt")

            # start command (vagrant destroy ) execution process, then wait
            v_destroy = subprocess.Popen(["vagrant", "destroy", "--force"], stdin=subprocess.PIPE)
            # now wait for command execution completion
            v_destroy.communicate(input='y')
            # assert that command executed successfully
            assert_success(v_destroy.returncode, "vagrant destroy")

            # start command (vagrant remove ) execution process, then wait
            v_remove = subprocess.Popen(["vagrant", "box", "remove", testConfig["box_name"]])
            # now wait for command execution completion
            v_remove.communicate()
            # assert that command executed successfully
            assert_success(v_remove.returncode, "vagrant box remove")

            # clean up
            subprocess.call(["rm", "-rf", v_dir])

