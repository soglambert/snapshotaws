from setuptools import setup

setup(
    name = 'snapshotaws',
    version = '0.1',
    author='Leilei',
    author_email='jalahealth@gmail.com',
    description='SnapshotAnalyzer is a tool to manage EC2 instances',
    license='GPLv3+',
    package=['shotty'],
    url = 'https://github.com/soglambert/snapshotaws',
    install_requires = [
        'click',
        'boto3'
    ],
    entry_points='''
        [console_script]
        shotty=shotty.shotty:cli
    ''',
)
