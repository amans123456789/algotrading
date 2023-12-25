from setuptools import setup
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.run(["python", "-m", "spacy", "download", "en"])

setup(
    name='your_package',
    version='1.0',
    packages=['your_package'],
    cmdclass={'install': PostInstallCommand},
    install_requires=[
        'spacy==3.7.2',
        # other dependencies
    ],
)