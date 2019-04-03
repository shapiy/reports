from setuptools import setup, find_packages

setup(
    name='reports',
    version='0.1.0',
    description='Send customized emails with Toggl time reports',
    author='shapiy',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'invoices = reports:main'
        ]
    }
)
