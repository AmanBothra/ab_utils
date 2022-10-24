'''
pytz setup script
'''
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

me = 'Aman Bothra'
memail = 'amanbothra1777@gmail.com'

packages = ['ab_utils']
package_dir = {'ab_utils': 'src/ab_utils'}

setup(
    name='ab_utils',
    version='0.1',
    zip_safe=True,
    description='Utility functions',
    author=me,
    author_email=memail,
    maintainer=me,
    maintainer_email=memail,
    url='https://github.com/AmanBothra/ab_utils',
    license=open('LICENSE', 'r').read(),
    keywords=['python', 'django'],
    packages=packages,
    package_dir=package_dir,
    platforms=['Independant'],
    classifiers=[
        'Development Status :: 1 - beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
