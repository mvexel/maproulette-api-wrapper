from setuptools import setup, find_packages

setup(
    name='maproulette',
    packages=['maproulette'],  # this must be the same as the name above
    version='0.2.9',
    description='A wrapper for the MapRoulette API',
    author='Martijn van Exel',
    author_email='m@rtijn.org',
    url='https://github.com/mvexel/maproulette-api-wrapper',
    download_url='https://github.com/mvexel/maproulette-api-wrapper/archive/0.2.8.tar.gz',
    keywords=['maproulette'],
    classifiers=[],
    install_requires=['requests']
)
