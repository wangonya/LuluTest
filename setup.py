from setuptools import setup, find_packages

setup(
    name='LuluTest',
    packages=find_packages(),
    version='0.1',
    license='apache-2.0',
    description='A suite of tools to un-complicate browser automation',
    author='Erik Whiting',
    author_email='erik@erikwhiting.com',
    url='https://github.com/erik-whiting/LuluTest',
    keywords=['testing', 'browser automation', 'webdriver'],
    install_requires=[
        'selenium',
        'urllib3',
        'pyyaml'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
