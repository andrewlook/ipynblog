from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

test_deps = [
  'future',
  'twine',
  'pytest',
  'pytest-mock',
  'python-coveralls'
]

extras = {
  'test': test_deps,
}

setup(
    name='ipynblog',
    version='0.1.0',
    description='Utility for converting jupyter/colab notebooks to static sites for publishing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andrewlook/ipynblog',
    author='Andrew Look',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='jupyter nbconvert publishing web development',  # Optional
    packages=find_packages(exclude=['docs', 'tests']),  # Required
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'pyyaml',
        'future',
        'six',
        'nbformat',
        'nbconvert',
        'jupyter',
        'jinja2',
    ],
    tests_require=test_deps,
    extras_require=extras,
    # installs the 'ipynblog' CLI command when users install via pip.
    entry_points={
        'console_scripts': [
            'ipynblog = ipynblog.__main__:main',
            'ipynblog-download = ipynblog.download:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/andrewlook/ipynblog/issues',
        'Source': 'https://github.com/andrewlook/ipynblog/',
    },
)
