from setuptools import setup, find_packages

setup(
    name='YourProjectName',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Other dependencies...
        'git+https://github.com/AI4Finance-Foundation/FinNLP.git',
    ],
)