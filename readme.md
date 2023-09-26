# Bench -- Laboratory Instrument Control

## Introduction

Bench is a lightweight package built on top of Pyvisa. As I have used Pyvisa to conduct laboratory work and test automation, I've found myself wanting one more abstraction layer on top. This package provides that framwork to interact with VISA-compatible test instruments in a more abstract way and allows the user to develop well documented and repeatable bench measurements while still harnessing the full feature set of their bench instruments. Properly implemented instrument drivers, which are low-level *inheritable* classes written for each instrument, use a common interface allowing for swapping one instrument for another with no changes to the test script.

This project is under active development.

## Goals of the project: 
    
    1.  Develop and maintain simple abstraction layer on top of PyVISA consisting of:
        a.  Instrument Abstract Class
        b.  Oscilloscope Abstract Class
        c.  Power Supply Abstract Class
        d.  Waveform Generator Abstract Class
        e.  Instrument Finder Class
        f.  Other types of test instruments as needed
    2.  Support the following instruments that I use in my lab
        a.  Keysight DSOX1204G
        b.  Tektronix MSO2014
        c.  Keysight E36303
        d.  Keithley 2231A-30-3
        e.  Keysight EDU22312

## Structure and supported instruments:

    .
    └── *Bench Package:*/
        ├── InstrumentFinder Class
        └── Instrument Abstract Class/
            ├── Oscilloscope Abstract Class/
            │   ├── Keysight DSOX1204G
            │   ├── Tektronix MSO2014B
            │   └── ...
            ├── Power Supply Abstract Class/
            │   ├── Keysight E36303A
            │   ├── Keithley 2231A-30-3
            │   └── ...
            └── Waveform Generator Abstract Class/
                ├── Keysight EDU22312 Class
                └── ...
