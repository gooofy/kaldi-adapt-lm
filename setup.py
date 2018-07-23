from setuptools import setup

setup(
    name                 = 'kaldi-adapt-lm',
    version              = '0.1.0',
    description          = 'Adapt Kaldi-ASR nnet3 chain models from Zamia-Speech.org to a different language model.',
    long_description     = open('README.md').read(),
    author               = 'Guenter Bartsch',
    author_email         = 'guenter@zamia.org',
    maintainer           = 'Guenter Bartsch',
    maintainer_email     = 'guenter@zamia.org',
    url                  = 'https://github.com/gooofy/kaldi-adapt-lm',
    packages             = ['kaldiadaptlm'],
    install_requires     = [ ],
    scripts              = [ 'kaldi-adapt-lm' ],
    classifiers          = [
                               'Operating System :: POSIX :: Linux',
                               'License :: OSI Approved :: Apache Software License',
                               'Programming Language :: Python :: 2',
                               'Programming Language :: Python :: 2.7',
                               'Intended Audience :: Developers',
                               'Topic :: Software Development :: Libraries :: Python Modules',
                               'Topic :: Multimedia :: Sound/Audio :: Speech'
                               'Topic :: Scientific/Engineering :: Artificial Intelligence'
                           ],
    license              = 'Apache',
    keywords             = 'natural language processing nlp asr speech recognition kaldi',
    package_data         = {'kaldiadaptlm': ['templates/*']},
    include_package_data = True
    )

