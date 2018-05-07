
from setuptools import setup
 
setup(
    name='ahabclient',
    version='0.0.13',
    license='Apache License 2.0',
    description='AHAB Docker Client Wrapper',
    author="Marco Montanari",
    author_email="marco.montanari@gmail.com",
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
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],

)