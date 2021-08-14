from setuptools import setup

setup(
    name = 'fastanalizer',
    packages = ['fastanalizer'],
    version = '0.1',
    license='MIT',
    description = 'Tool for fast protein domain analysis',
    author = 'Alexandre Zanatta Vieira',
    author_email = 'al-zanatta@hotmail.com',
    url = 'https://github.com/alezanatta/fastanalizer',
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['BIOINFORMATICS', 'PROTEIN', 'PHYLOGENY'],
    entry_points={
        'console_scripts': [
            'fastanalizer = fastanalizer:main'
        ]
    },
    install_requires=[
            'plotly<5',
            'biopython>=1.77',
            'numpy>=1',
            'pandas>=1',
            'scikit-learn',
            'requests>=2.21'
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: General',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
)