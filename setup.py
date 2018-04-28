
from setuptools import setup
 
setup(
    name='ahabclient',
    version='0.0.4',
    license='MIT',
    py_modules=['ahab'],
    entry_points={
        'console_scripts':[
            'ahab=ahab:main',
        ]
    },
    install_requires=[
        'requests',
        'docker',
        'semantic_version',
    ]

)