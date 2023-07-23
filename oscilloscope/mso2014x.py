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
"""_summary_

Returns:
    _description_
"""

from datetime import datetime as dt
from time import struct_time
from typing import Self

from .. import bench


class MSO2014x(bench.Instrument):
    """
   Class containing interface for the Tektronix MSO2014(B).

    Parent Class:
        Instrument
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

        print("INSTRUMENT INITIALIZED")  # write initialization message

    def system_lock(self) -> Self:
        """
        Disable front panel controls
        """

        self.write("lock")  # disable front panel controls
        return self

    def system_unlock(self) -> Self:
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
        # there are two sections to each message here, the command and the label itself
        # the command section is the one that varies, so the label code can stay the same each time

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
    
    def set_input_params(self, n_bits: int, binary_format: str, n_bytes: int, byte_order: str, 
                     composition: str, encoding: str, filter_frequency: int, n_points: int, 
                     point_format: str, point_offset: int, x_increment: float, x_unit: str, 
                     x_zero: float, y_multiplier: float, y_offset: float, y_unit: str, 
                     y_zero: float) -> Self:
        
        """
        This method sets the parameters for the waveform prior to acquisition
        
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
        # there is probably a better way to do this, and a better place to do it
        # need this later
        units = ["%", "/Hz", "A", "A/A", "A/V", "A/W", "A/dB", "A/s", "AA", "AW", "AdB", "As", "B", "Hz", "IRE", "S/s", "V", "V/A", "V/V", "V/W", "V/dB", "V/s", "VV", "VW", "VdB", "Volts", "Vs", "W", "W/A", "W/V", "W/W", "W/dB", "W/s", "WA", "WV", "WW", "WdB", "Ws", "dB", "dB/A", "dB/V", "dB/W", "dB/dB", "dBA", "dBV", "dBW", "dBdB", "day", "degrees", "div", "hr", "min", "ohms", "percent", "s"] # pulled from programmers guide page 2-359
        
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
                
    def get_input_params(self) -> Self:
        """
        This method gets the parameters for the waveform prior to acquisition and returns a list
        
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
        n_bits: int = self.query(f"wfminpre:bit_nr?")

        # get binary format for waveform data - signed or unsigned integer    
        binary_format: str = self.query(f"wfminpre:bn_fmt?")

        # get number of bytes for waveform data - 1-byte or 2-byte
        n_bytes: int = self.query(f"wfminpre:byt_nr?")

        # get byte order for waveform data - least-significant-byte or most-significant-byte
        byte_order: str = self.query(f"wfminpre:byt_or?")

        # get the type of waveform data to be transferred
        composition: str = self.query(f"wfminpre:composition?")

        # get the encoding for the waveform data - either ascii or binary
        encoding: str = self.query(f"wfminpre:encdg?")
        
        # get the digital filter frequency for the waveform data
        filter_frequency: int = self.query(f"wfminpre:filterfreq?")

        # get the number of points to acquire
        n_points: int = self.query(f"wfminpre:nr_pt?")
        
        # get the point format - envelope or singular
        point_format: str = self.query(f"wfminpre:pt_fmt?")
        
        # get point offset - unsused
        point_offset: int = self.query(f"wfminpre:pt_off?")

        # get the x increment, measured in units of x_unit
        x_increment: float = self.query(f"wfminpre:xincr?")
        
        # get the x unit for the waveform data
        x_unit: str = self.query(f"wfminpre:xunit?")

        # get the position value in x_unit of the first sample of the incoming waveform
        x_zero: float = self.query(f"wfminpre:xzero?")

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
        This method gets the parameters for the waveform following acquisition and returns a list
        
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

## TODO BELOW
'''
    def get_settings(self) -> list[str]:
        """
        Returns settings of current channel

        Returns:
            channel_settings -- returns channel range, offset,
            coupling, impedance, display status, bandwidth limit,
            inversion status, units, probe status, probe skew,
            and signal type
        """

        return self.query(f"channel{self.current_channel}?")

    def set_trigger_level(self, trigger_level) -> None:
        """
        _summary_

        Arguments:
            trigger_level -- _description_
        """

        self.write(
            f"trigger:level {trigger_level}, channel{self.current_channel}")

    def get_trigger_level(self) -> float:
        """
        _summary_

        Returns:
            _description_
        """

        return self.query("trigger:level?")

    def set_range(self, v_range) -> None:
        """
        Sets the vertical range of the current channel

        Arguments:
            v_range -- range to set for the current channel -> +/- range/2
        """

        self.write(
            f"channel{self.current_channel}:range {v_range}")

    def get_range(self) -> float:
        """
        Gets the vertical range of the current channel

        Returns:
            float(v_range) -- vertical range cast to float
        """

        return self.query(f"channel{self.current_channel}:range?")

    def set_attenuation(self, attenuation) -> None:
        """
        Sets the level of attenuation for the current channel. Floating point number from 1-1000

        Arguments:
            attenuation -- attenuation factor to write to current channel
        """

        self.write(
            f"channel{self.current_channel}:probe {float(attenuation)}")

    def get_attenuation(self) -> float:
        """
        Gets the attenuation factor for the current channel

        Returns:
            Current channel attenuation factor
        """

        return self.query(f"channel{self.current_channel}:probe?")

    def set_offset(self, offset) -> None:
        """Sets the waveform offset for the current channel

        Arguments:
            offset -- floating point value for the offset
        """

        self.write(
            f"channel{self.current_channel}:offset {float(offset)}")

    def get_offset(self) -> float:
        """Gets the waveform offset for the current channel

        Returns:
            waveform offset value for the current channel
        """

        return self.query(f"channel{self.current_channel}:offset?")

    def set_coupling(self, coupling) -> None:
        """Sets the coupling mode for the current channel. AC or DC.

        Arguments:
            coupling -- string - ac or dc

        Returns:
            Coupling type error
        """

        match coupling:

            case "":
                if self.get_coupling().lower() == 'ac':
                    self.write(
                        f"channel{self.current_channel}:coupling dc")

                else:
                    self.write(
                        f"channel{self.current_channel}:coupling ac")

            case "dc" | "Dc" | "DC":
                self.write(
                    f"channel{self.current_channel}:coupling dc")

            case "ac" | "Ac" | "AC":
                self.write(
                    f"channel{self.current_channel}:coupling ac")

            case _:  # TODO
                pass

    def get_coupling(self) -> str:
        """
        Gets the current channel's coupling mode

        Returns:
            coupling type
        """

        return self.query(
            f"channel{self.current_channel}:coupling?")

    def get_impedance(self) -> str:
        """
        Gets the impedance of the current channel. Most oscilloscopes cannot change the input
        impedance.

        Returns:
            input impedance
        """

        return self.query(f"channel{self.current_channel}:impedance?")

    def set_display(self, status) -> None:
        """Sets the Boolean value for the display of the current channel -> 1 == ON and 0 == OFF

        Arguments:
            status -- boolean value, is the current channel displayed?

        Returns:
            Display Error
        """

        match status:

            case "":
                if not self.get_display():
                    self.write(
                        f"channel{self.current_channel}:display on")

                else:
                    self.write(
                        f"channel{self.current_channel}:display off")

            case "on" | "ON" | "On" | 1 | True:
                self.write(
                    f"channel{self.current_channel}:display on")

            case "off" | "OFF" | "Off" | 0 | False:
                self.write(
                    f"channel{self.current_channel}:display off")

            case _:  # TODO
                pass

    def get_display(self) -> bool:
        """
        Gets the status of the display for the current channel. Is the current channel's
        waveform displayed?

        Returns:
            Display status for the current channel
        """

        return self.query(
            f"channel{self.current_channel}:display?")

    def set_bwlimit(self, status) -> None:
        """
        Sets the bandwidth limit for the current channel

        Arguments:
            status -- status of the bandwidth limiter circuitry
        """

        match status:

            case "":
                if not self.get_bwlimit():
                    self.write(
                        f"channel{self.current_channel}:bwlimit on")

                else:
                    self.write(
                        f"channel{self.current_channel}:bwlimit off")

            case "on" | "ON" | "On" | 1 | True:
                self.write(
                    f"channel{self.current_channel}:bwlimit on")

            case "off" | "OFF" | "Off" | 0 | False:
                self.write(
                    f"channel{self.current_channel}:bwlimit off")

            case _:  # TODO
                pass

    def get_bwlimit(self) -> bool:
        """
        Gets the status of the bandwidth limiter circuit

        Returns:
            boolean status of the bandwidth limiter circuit
        """

        return self.query(f"channel{self.current_channel}:bwlimit?")

    def set_wfinvert(self, status) -> None:
        """
        Sets the waveform inversion status. On or Off

        Arguments:
            status -- inversion status, boolean

        Returns:
            Waveform Inversion Error
        """

        match status:

            case "":
                if not self.get_wfinvert():
                    self.write(
                        f"channel{self.current_channel}:invert on")
                else:
                    self.write(
                        f"channel{self.current_channel}:invert off")

            case "on" | "ON" | "On" | 1 | True:
                self.write(
                    f"channel{self.current_channel}:invert on")

            case "off" | "OFF" | "Off" | 0 | False:
                self.write(
                    f"channel{self.current_channel}:invert off")

            case _:  # TODO
                pass

    def get_wfinvert(self) -> bool:
        """
        Gets the waveform inversion status for the current channel

        Returns:
            waveform inversion status for the current channel
        """

        return self.query(
            f"channel{self.current_channel}:invert?")

    def set_unit(self, unit) -> None:
        """
        Sets the unit for the current channel

        Arguments:
            unit -- unit, usually Volts or Amps

        Returns:
            Unit Error
        """

        match unit:

            case "":
                if self.get_unit().lower() == 'amp':
                    self.write(
                        f"channel{self.current_channel}:unit volt")
                else:
                    self.write(
                        f"channel{self.current_channel}:unit amp")

            case "volt" | "VOLT" | "Volt" | "voltage" | "Voltage" | "VOLTAGE":
                self.write(
                    f"channel{self.current_channel}:unit volt")

            case "amp" | "AMP" | "Amp" | "ampere" | "Ampere" | "AMPERE":
                self.write(
                    f"channel{self.current_channel}:unit amp")

            case _:  # TODO
                pass

    def get_unit(self) -> str:
        """
        Gets the units for the current channel

        Returns:
            unit for the current channel
        """

        return self.query(f"channel{self.current_channel}:unit?")

    def set_sigtype(self, sigtype: str) -> None:
        """Sets the type of signal for the current channel

        Arguments:
            sigtype -- single-ended or differential

        Returns:
            Signal Type Error
        """

        match sigtype.lower():

            case "":
                if self.get_sigtype().lower() == 'sing':
                    self.write(
                        f"channel{self.current_channel}:stype differential")

                else:
                    self.write(
                        f"channel{self.current_channel}:stype single")

            case "single" | "single-ended" | "sing":
                self.write(
                    f"channel{self.current_channel}:stype single")

            case "differential" | "diff":
                self.write(
                    f"channel{self.current_channel}:stype differential")

            case _:  # TODO
                pass

    def get_sigtype(self) -> str:
        """
        Gets the type of signal for the current channel

        Returns:
            signal type for the current channel
        """

        return self.query(f"channel{self.current_channel}:stype?")
'''
