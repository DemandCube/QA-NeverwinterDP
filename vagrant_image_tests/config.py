"""
box with url="" will be skipped from testing
"""

check_config = [
    {
        "box_name": "ubuntu1304",
        "box_url": "file:///home/hikmat/contributions/vagrant-ubuntu/boxes/ubuntu1304-x86_64-20140303.box",
        "packages": [
            {
                "name": "ansible",
                "binary": "ansible"
            },
            {
                "name": "pip",
                "binary": "pip"
            }
        ],
        "prerequisites": [
            {
                "name": "virtualbox",
                "binary": "virtualbox"
            },
            {
                "name": "vagrant",
                "binary": "vagrant"
            }
        ]
    }
]
