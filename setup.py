from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='financial_rsi_bot',
    version='1.0.0',
    author='Tergel Munkhbaatar',
    author_email='tergelitu@gmail.com',
    description='A bot to analyze and visualize price data using the RSI indicator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tergelitu/tradebot.v1.o',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'yfinance',
        'pandas',
        'matplotlib',
        'mplfinance',
        'GoogleNews',
        'textblob',
        'tweepy',
        'colorama',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'run-analysis=teddy.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)
