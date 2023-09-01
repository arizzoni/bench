#!/usr/bin/env python3.11

'''
    Bench -- Laboratory Instrument Control
    Copyright (C) 2023 Alessandro Rizzoni

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.
'''

from datetime import datetime as dt
from time import struct_time
from typing import Self

from .. import bench


class MSO2014x(bench.Instrument):
    """
    Class containing interface for the Tektronix MSO2014(B).
    Inherits from bench.Instrument.
    """

    current_channel: int = 1  # initialize to channel 1
    num_channels: int = 4  # TODO pull this from the instrument
    channel_list: list[int] = list(range(1, num_channels+1))

    def __init__(self, address: str) -> None:
        """
        Constructor for the Oscilloscope class; connects to oscilloscope at {address}

        Arguments:
            address -- target oscilloscope's VISA address
        """

        bench.Instrument.__init__(
            self, address)  # call parent class constructor for basic init

        # set the date and time
        time: struct_time = dt.now().timetuple()
        self.write(f"date {time[0]}, {time[1]}, {time[2]}")
        self.write(f"time {time[3]}, {time[4]}, {time[5]}")
        
        # there is probably a better way to do this  
        units = ["%", "/Hz", "A", "A/A", "A/V", "A/W", "A/dB", "A/s", "AA", "AW", 
                 "AdB", "As", "B", "Hz", "IRE", "S/s", "V", "V/A", "V/V", "V/W", 
                 "V/dB", "V/s", "VV", "VW", "VdB", "Volts", "Vs", "W", "W/A", "W/V", 
                 "W/W", "W/dB", "W/s", "WA", "WV", "WW", "WdB", "Ws", "dB", "dB/A", 
                 "dB/V", "dB/W", "dB/dB", "dBA", "dBV", "dBW", "dBdB", "day", 
                 "degrees", "div", "hr", "min", "ohms", "percent", "s"] # pulled from programmers guide page 2-359
        
        print("INSTRUMENT INITIALIZED")  # write initialization message

    def lock(self) -> Self:
        """
        Disable front panel controls
        """

        self.write("lock")  # disable front panel controls
        return self

    def unlock(self) -> Self:
        """
        Enable front panel controls
        """

        self.write("unlock")  # disable front panel controls
        return self

    def channel(self, channel_number: int) -> Self | None:
        """
        sets the oscilloscope channel to operate on

        Arguments:
            channel_number -- number of channel to select

        Returns:
            self - returns parent object for second method call
        """

        match channel_number:
            case chan if chan in self.channel_list:  # if a real channel is selected,
                self.current_channel = channel_number # set current_channel to selected channel
                return self  # return instance
            case _:  # otherwise return an error message
                raise Exception("Channel Number Error: Channel out of range")

    def set_label(self, channel: int, label: str = "Channel {channel}") -> None:
        """
        Writes waveform labels to the oscilloscope screen

        Arguments:
            text -- label text, written to oscilloscope screen
            channel -- desired channel to label
        """

        match channel:
            case chan if chan in self.channel_list:  # if a real channel is selected,
                self.write(f"ch{channel}:label \"{label}\"") # label it
            case _:  # otherwise return an error message
                raise Exception("Channel Number Error: Channel out of range")

        return self

    def autoscale(self) -> Self:
        """
        Autoscales current channel
        """
        
        # refactor to have the same behavior as DSOX?
        self.write("autoset enable")
        return self    
    
    def set_input_params(self, n_bits: int, binary_format: str, n_bytes: int, byte_order: str, composition: str, encoding: str, filter_frequency: int, n_points: int, point_format: str, point_offset: int, x_increment: float, x_unit: str, x_zero: float, y_multiplier: float, y_offset: float, y_unit: str, y_zero: float) -> Self:
        
        """
        Sets the parameters for the waveform prior to acquisition
        
        Arguments:
            n_bits
            binary_format
            n_bytes
            byte-order
            composition
            encoding
            filter_frequency
            n_points
            point_format
            point_offset
            x_increment
            x_unit
            x_zero
            y_multiplier
            y_offset
            y_unit
            y_zero
        
        Returns:
        Self
        
        """
        
        # set number of bits for waveform data - 8-bit or 16-bit
        # also changes byte number
        if n_bits:
            match n_bits:
                case 8, 16:
                    self.write(f"wfminpre:bit_nr {int(n_bits)}")
                case _:
                    raise Exception("Bit Number Error: Only 8-bit and 16-bit allowed")

        # set binary format for waveform data - signed or unsigned integer    
        if binary_format:
            match binary_format:
                case "signed", "unsigned":
                    if binary_format == "signed":
                        binary_format == "RI"
                    else:
                        binary_format == "RP"
                    self.write(f"wfminpre:bn_fmt {str(binary_format)}")
                case _:
                    raise Exception("Binary Format Error: Only signed and unsigned integer formats allowed")

        # set number of bytes for waveform data - 1-byte or 2-byte
        # also changes bit number
        if n_bytes:
            match n_bytes:
                case 1, 2:
                    self.write(f"wfminpre:byt_nr {int(n_bytes)}")
                case _:
                    raise Exception("Byte Number Error: Only 1-byte and 2-byte allowed")

        # set binary format for waveform data - signed or unsigned integer    
        if binary_format:
            match binary_format:
                case "signed", "unsigned":
                    if binary_format == "signed":
                        binary_format == "RI"
                    else: 
                        binary_format == "RP"
                    self.write(f"wfminpre:bn_fmt {str(binary_format)}")
                case _:
                    raise Exception("Binary Format Error: Only signed and unsigned integer formats allowed")

        # set byte order for waveform data - least-significant-byte or most-significant-byte
        if byte_order:
            match byte_order:
                case "lsb", "msb":
                    self.write(f"wfminpre:byt_or {str(byte_order)}")
                case _:
                    raise Exception("Byte Order Error: Only least-significant-byte (lsb) and most-significant-byte (msb) allowed")

        # set the type of waveform data to be transferred
        if composition:
            match composition:
                case "composite", "peak-detect", "singular":
                    if composition == "composite":
                        composition = "composite_yt"
                    elif composition == "peak-detect":
                        composition = "composite_env"
                    else: 
                        composition = "singular_yt"
                    self.write(f"wfminpre:composition {str(composition)}")
                case _:
                    raise Exception("Composition Error: Only composite, peak-detect, and singular allowed")

        # set the encoding for the waveform data - either ascii or binary
        if encoding:
            match encoding:
                case "ascii", "binary":
                    self.write(f"wfminpre:encdg {str(encoding)}")
                case _:
                    raise Exception("Encoding Error: Only ascii and binary encodings are allowed")

        # set the digital filter frequency for the waveform data
        if filter_frequency:
            self.write(f"wfminpre:filterfreq {int(filter_frequency)}")
            # TODO raise Exception("Filter Frequency Error: Invalid frequency selected")

        # set the number of points to acquire
        if n_points:
            self.write(f"wfminpre:nr_pt {int(n_points)}")
            # TODO raise Exception("Point Number Error: Invalid number of points")
        
        # set the point format - envelope or singular
        if point_format:
            match point_format:
                case "envelope", "singular":
                    self.write(f"wfminpre:encdg {str(encoding)}")
                case _:
                    raise Exception("Encoding Error: Only ascii and binary encodings are allowed")
        
        # set point offset - unsused
        if point_offset:
            self.write(f"wfminpre:pt_off {int(point_offset)}")

        # set the x increment, measured in units of x_unit
        if x_increment:
            self.write(f"wfminpre:xincr {float(x_increment)}")
        
        # set the x unit for the waveform data
        if x_unit:
            
            match x_unit:
                case unit if unit in units:
                    self.write(f"wfminpre:xunit {str(x_unit)}")
                case _:
                    raise Exception("Unit Error: invalid unit")

        # set the position value in x_unit of the first sample of the incoming waveform
        if x_zero:
            self.write(f"wfminpre:xzero {float(x_zero)}")

        # set the vertical scale factor for the waveform data
        if y_multiplier:
            self.write(f"wfminpre:ymult {float(y_multiplier)}")       
        
        # set the vertical offset for the waveform data    
        if y_offset:
            self.write(f"wfminpre:yoff {float(y_offset)}")        
        
        # set the y unit for the waveform data
        if y_unit:
            match y_unit:
                case unit if unit in units:
                    self.write(f"wfminpre:yunit {str(y_unit)}")
                case _:
                    raise Exception("Unit Error: invalid unit")        
        
        # set the y value, in units of y_unit, of the first data point        
        if y_zero:
            self.write(f"wfminpre:yzero {float(y_zero)}")        

    def get_input_bit_nr(self) -> int:    
        """
        Gets the number of bits for waveform data - 8-bit or 16-bit
        
        Returns:
        """

        return self.query(f"wfminpre:bit_nr?")
    
    def get_input_bn_fmt(self) -> str:    
        """
        Gets the binary format for waveform data - signed or unsigned integer
        
        Returns:
        """  

        return self.query(f"wfminpre:bn_fmt?")
    
    def get_input_byt_nr(self) -> int:    
        """
        Gets the number of bytes for waveform data - 1-byte or 2-byte
        
        Returns:
        """

        return self.query(f"wfminpre:byt_nr?")
    
    def get_input_byt_or(self) -> str: 
        """
        Gets the byte order for waveform data - least-significant-byte or most-significant-byte
        
        Returns:
        """

        return self.query(f"wfminpre:byt_or?")
    
    def get_input_composition(self) -> str:    
        """
        Gets the type of waveform data to be transferred
        
        Returns:
        """

        return self.query(f"wfminpre:composition?")
    
    def get_input_encdg(self) -> str:    
        """
        Gets the encoding for the waveform data - either ascii or binary
        
        Returns:
        """

        return self.query(f"wfminpre:encdg?")
    
    def get_input_filterfreq(self) -> float:    
        """
        Gets the digital filter frequency for the waveform data
        
        Returns:
        """

        return self.query(f"wfminpre:filterfreq?")
    
    def get_input_nr_pt(self) -> int:    
        """
        Gets the number of points to acquire
        
        Returns:
        """

        return self.query(f"wfminpre:nr_pt?")
    
    def get_input_pt_fmt(self) -> str:    
        """
        Gets the point format - envelope or singular
        
        Returns:
        """

        return self.query(f"wfminpre:pt_fmt?")
    
    def get_input_pt_off(self) -> int:    
        """
        Gets the point offset - unsused
        
        Returns:
        """    

        return self.query(f"wfminpre:pt_off?")
    
    def get_input_x_incr(self) -> float:    
        """

        Gets the x increment, measured in units of x_unit
        
        Returns:
        """

        return self.query(f"wfminpre:xincr?")
    
    def get_input_x_unit(self) -> str:    
        """
        Gets the x unit for the waveform data
        
        Returns:
        """ 

        return self.query(f"wfminpre:xunit?")
    
    def get_input_x_zero(self) -> float:    
        """
        Gets the position value in x_unit of the first sample of the incoming waveform
        
        Returns:
        """

        return self.query(f"wfminpre:xzero?")
    
    def get_input_y_mult(self) -> float:    
        """
        Gets the vertical scale factor for the waveform data
        
        Returns:
        """

        return self.query(f"wfminpre:ymult?")      
     
    def get_input_y_offset(self) -> float:    
        """
        Gets the vertical offset for the waveform data
        
        Returns:
        """

        return self.query(f"wfminpre:yoff?")
            
    def get_input_y_unit(self) -> str:
        """    
        Gets the y_unit from the waveform input preamble
        
        Arguments: 
            None
        
        Returns: y unit string
        """

        return self.query(f"wfminpre:yunit?")       
        
    def get_input_y_zero(self) -> float:
        """
        Gets the y_zero value from the waveform input preamble
        
        Arguments:
            None
        
        Returns: y value, in units of y_unit, of the first data point
        """

        return self.query(f"wfminpre:yzero?")  

    def get_input_params(self) -> Self:
        """
        Gets the parameters for the waveform prior to acquisition and returns a list
        
        Arguments:
            None
        
        Returns:
            List(
                n_bits
                binary_format
                n_bytes
                byte-order
                composition
                encoding
                filter_frequency
                n_points
                point_format
                point_offset
                x_increment
                x_unit
                x_zero
                y_multiplier
                y_offset
                y_unit
                y_zero
            )
        """   

        # get number of bits for waveform data - 8-bit or 16-bit
        n_bits: int = self.get_input_bit_nr()

        # get binary format for waveform data - signed or unsigned integer    
        binary_format: str = self.get_input_bn_fmt()

        # get number of bytes for waveform data - 1-byte or 2-byte
        n_bytes: int = self.get_input_byt_nr()

        # get byte order for waveform data - least-significant-byte or most-significant-byte
        byte_order: str = self.get_input_byt_or()

        # get the type of waveform data to be transferred
        composition: str = self.get_input_composition()

        # get the encoding for the waveform data - either ascii or binary
        encoding: str = self.get_input_encdg()
        
        # get the digital filter frequency for the waveform data
        filter_frequency: int = self.get_input_filterfreq

        # get the number of points to acquire
        n_points: int = get_input_nr_pt()
        
        # get the point format - envelope or singular
        point_format: str = self.get_input_pt_fmt()
        
        # get point offset - unsused
        point_offset: int = self.get_input_pt_off()

        # get the x increment, measured in units of x_unit
        x_increment: float = self.get_input_x_incr()
        
        # get the x unit for the waveform data
        x_unit: str = self.get_input_x_unit()

        # get the position value in x_unit of the first sample of the incoming waveform
        x_zero: float = self.get_input_x_zero()

        # get the vertical scale factor for the waveform data
        y_multiplier: float = self.query(f"wfminpre:ymult?")       
        
        # get the vertical offset for the waveform data    
        y_offset: float = self.query(f"wfminpre:yoff?")        
        
        # get the y unit for the waveform data
        y_unit: str = self.query(f"wfminpre:yunit?")       
        
        # get the y value, in units of y_unit, of the first data point        
        y_zero: float = self.query(f"wfminpre:yzero?")  
          
        return [n_bits, binary_format, n_bytes, byte_order, composition, encoding, filter_frequency, n_points, point_format, point_offset, x_increment, x_unit, x_zero, y_multiplier, y_offset, y_unit, y_zero]

    def get_output_params(self) -> Self:
        """
        Gets the parameters for the waveform following acquisition and returns a list
        
        Arguments:
            None
        
        Returns:
            List(
                n_bits
                binary_format
                n_bytes
                byte-order
                composition
                encoding
                filter_frequency
                n_points
                point_format
                point_offset
                x_increment
                x_unit
                x_zero
                y_multiplier
                y_offset
                y_unit
                y_zero
            )
        """  

        # get number of bits for waveform data - 8-bit or 16-bit
        n_bits: int = self.query(f"wfmoutpre:bit_nr?")

        # get binary format for waveform data - signed or unsigned integer    
        binary_format: str = self.query(f"wfmoutpre:bn_fmt?")

        # get number of bytes for waveform data - 1-byte or 2-byte
        n_bytes: int = self.query(f"wfmoutpre:byt_nr?")

        # get byte order for waveform data - least-significant-byte or most-significant-byte
        byte_order: str = self.query(f"wfmoutpre:byt_or?")

        # get the type of waveform data to be transferred
        composition: str = self.query(f"wfmoutpre:composition?")

        # get the encoding for the waveform data - either ascii or binary
        encoding: str = self.query(f"wfmoutpre:encdg?")
        
        # get the digital filter frequency for the waveform data
        filter_frequency: int = self.query(f"wfmoutpre:filterfreq?")

        # get the number of points to acquire
        n_points: int = self.query(f"wfmoutpre:nr_pt?")
        
        # get the point format - envelope or singular
        point_format: str = self.query(f"wfmoutpre:pt_fmt?")
        
        # get point offset - unsused
        point_offset: int = self.query(f"wfmoutpre:pt_off?")

        # get the x increment, measured in units of x_unit
        x_increment: float = self.query(f"wfmoutpre:xincr?")
        
        # get the x unit for the waveform data
        x_unit: str = self.query(f"wfmoutpre:xunit?")

        # get the position value in x_unit of the first sample of the incoming waveform
        x_zero: float = self.query(f"wfmoutpre:xzero?")

        # get the vertical scale factor for the waveform data
        y_multiplier: float = self.query(f"wfmoutpre:ymult?")       
        
        # get the vertical offset for the waveform data    
        y_offset: float = self.query(f"wfmoutpre:yoff?")        
        
        # get the y unit for the waveform data
        y_unit: str = self.query(f"wfmoutpre:yunit?")       
        
        # get the y value, in units of y_unit, of the first data point        
        y_zero: float = self.query(f"wfmoutpre:yzero?")  
          
        return [n_bits, binary_format, n_bytes, byte_order, composition, encoding, filter_frequency, n_points, point_format, point_offset, x_increment, x_unit, x_zero, y_multiplier, y_offset, y_unit, y_zero]

## TODO
'''
   trigger
    vertical range
    timebase
    attenuation?
    offset
    coupling
    impedance
    unit
    signal type
    waveform invert
    bw limit 
    '''
