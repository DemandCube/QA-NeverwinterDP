import subprocess
from installation_tests import assertionFunctions
from vagrant_image_tests import config

__author__ = 'hikmat'


def test_image_installation():
    for testConfig in config.check_config:
        if testConfig["box_url"] != "":
            if "prerequisites" in testConfig:
                    for innerTestConfig in testConfig["prerequisites"]:
                        if "binary" in innerTestConfig:
                            yield assertionFunctions.checkIfWhichCanFindBinary, innerTestConfig

            subprocess.call(["vagrant", "box", "add", testConfig["box_name"], testConfig["box_url"]])
            subprocess.call(["vagrant", "init", testConfig["box_name"]])
            subprocess.call(["vagrant", "up"])
            subprocess.call(["vagrant", "ssh", "-c", "touch /vagrant/Testfile.txt"])

            if "packages" in testConfig:
                for packageTestConfig in testConfig["packages"]:
                    if "binary" in packageTestConfig:
                        assert "name" in packageTestConfig
                        vagrant_ssh_command = subprocess.call(["vagrant", "ssh", "-c", "which" + " " + packageTestConfig["binary"]])
                        assert_success(vagrant_ssh_command)

            subprocess.call(["vagrant", "halt"])

            subprocess.call(["vagrant", "destroy"])

            subprocess.call(["vagrant", "box", "remove", testConfig["box_name"]])

            subprocess.call(["rm", "-rf", ".vagrant"])
            subprocess.call(["rm", "Testfile.txt"])
            subprocess.call(["rm", "Vagrantfile"])


def assert_success(result):
    assert str(result) == str(0), "Return Code: >>>>> %s" % result + ">>>>>Test Failed!!! \n ERROR: >>>>> %s" % str(result)
