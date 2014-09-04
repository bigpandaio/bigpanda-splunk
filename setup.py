from distutils.core import setup
 
setup(
    name='bigpanda-splunk',
    version='0.9.0',
    packages=['bigpanda_splunk'],
    license='LICENSE',
    description='BigPanda Splunk Integration',
    long_description=open('README.md').read(),
    author='BigPanda',
    author_email='support at bigpanda io',
    install_requires=[],
    scripts=['bin/bigpanda-splunk', 'bin/bigpanda-splunk-configure']
)
