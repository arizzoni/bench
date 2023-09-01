# Bench -- Laboratory Instrument Control

## Introduction

Bench is a lightweight package built on top of Pyvisa. It interfaces with USB- or LAN-connected VISA-compatible test instruments and allows the user to develop well documented and repeatable bench measurements while harnessing the full feature set of their bench instruments. This project is under active development - it is not suitable for use at this time.

The intention of this module is to provide the ability to use Jupyter Notebooks and this package to develop an open-source, easy to use notebook-style workflow for electronics design and analysis. For laboratory automation, I recommend https://github.com/usnistgov/labbench which offers extended capability for more advanced usage.

Goals of the project: 
    
    1.  Develop and maintain simple abstraction layer on top of PyVISA
    2.  Support instruments that I use in my lab

Structure and supported instruments:
.
└── bench.py/
    └── Instruments/
        ├── Oscilloscope/
        │   ├── Keysight DSOX1204G
        │   └── Tektronix MSO2014B
        ├── Power Supply/
        │   ├── Keysight E36303A
        │   └── Keithley 2231A-30-3
        ├── Arbitrary Function Generator/
        │   └── Keysight EDU22312
        └── ...
Each instrument has a configuration file that adheres to a standard interface.
