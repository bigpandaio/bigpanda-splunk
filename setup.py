from distutils.core import setup
 
setup(
    name='bigpanda-splunk',
    version='0.9.0',
    packages=['bigpanda_splunk'],
    license='apache v2',
    url="https://github.com/bigpandaio/bigpanda-splunk",
    description='BigPanda Splunk Action Script',
    long_description=open('README').read(),
    author='BigPanda',
    author_email='support at bigpanda io',
    scripts=['bin/bigpanda-splunk', 'bin/bigpanda-splunk-configure', 'bin/bigpanda-splunk-default']
)
