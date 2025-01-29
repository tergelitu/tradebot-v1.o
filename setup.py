from setuptools import setup, find_packages

setup(
    name='financial_rsi_bot',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'yfinance',
        'pandas',
        'matplotlib',
        'mplfinance',
    ],
    entry_points={
        'console_scripts': [
            'run-analysis=main:main',
        ],
    },
)
