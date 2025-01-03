from setuptools import setup

setup(name='mindwavemobile',
      version='0.200',
      description='Small Library to access NeuroSky MindWave Mobile functionality from Python',
      url='https://github.com/robintibor/python-mindwave-mobile',
      author='Robin Tibor Schirrmeister',
      author_email='robintibor@gmail.com',
      packages=['mindwavemobile'],
      install_requires=[
          'pybluez',
      ],
      zip_safe=False)
