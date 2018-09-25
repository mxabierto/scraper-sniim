from setuptools import setup, find_packages
import sniim


setup(
    name='sniim',
    description='Scraper de precios de productos basicos basado en la pagina del SNIIM',
    version='1.0.0',
    author='Francisco Vaquero',
    author_email='francisco@opi.la',
    install_requires=[
        'beautifulsoup4==4.6.3',
        'requests==2.19.1',
        'click==6.7',
        'pymongo==3.7.1',
        'clint==0.5.1',
        'pyfiglet==0.7.5',
        'python-dateutil==2.6.1'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sniim=sniim.cli:parse'
        ]
    }
)
