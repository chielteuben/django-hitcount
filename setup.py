import os
from setuptools import setup, find_packages
from hitcount import get_version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-hitcount",
    version = get_version(),
    url = 'http://github.com/vosi/django-hitcount',
    license = 'BSD',
    description = "Django hit counter application that tracks the number of hits/views for chosen objects",
    long_description = read('README.md'),

    author = 'VoSi',
    author_email = 'fon.vosi@gmail.com',

    packages = find_packages(),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
