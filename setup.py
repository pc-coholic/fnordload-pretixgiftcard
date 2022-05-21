try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='fnordload_pretixgiftcard',
    version='1.0.0',
    description='Fnordload for pretix gift card generation',
    author='',
    author_email='',
    url='https://github.com/pc-coholic/fnordload-pretixgiftcard',
    packages=['fnordload_pretixgiftcard'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='GPLv3+',
    install_requires=[
        'pyserial',
        'eSSP @ git+https://github.com/pc-coholic/eSSP@py3',
        'lcd2usb',
        'requests',
        'python-escpos @ git+https://github.com/python-escpos/python-escpos.git@master'
    ],
    scripts=['scripts/fnordload.py']
)