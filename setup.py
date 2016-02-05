from setuptools import setup, find_packages


print(find_packages())

setup(
    name='HEpigram',
    version='0.1',
    url='asdf',
    author='asdf',
    author_email='asdf',
    description=('asdf'),
    license='MIT',
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        hepigram=hepigram.app:cli
    '''
)
