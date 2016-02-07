from setuptools import setup, find_packages


print(find_packages())

setup(
    name='HEpigram',
    version='0.1',
    url='https://dev.hackerexperience.com/diffusion/HEPG/',
    author='Renato Massaro',
    author_email='renato@hackerexperience.com',
    description=('HEpigram provides a friendly interface for documents that '
                 'need to be generated/compiled by tools like MkDocs.'),
    license='MIT',
    packages=find_packages(),
    keywords=['documentation'],
    entry_points='''
        [console_scripts]
        hepigram=hepigram.app:cli
    '''
)
