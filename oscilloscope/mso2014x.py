#!/usr/bin/env python

""" Module Docstring
    
    ...

    ...


TODO
trigger
vertical range
horizontal timebase
attenuation
coupling
offset
waveform inversion
impedance
signal type
waveform invert
bw limit
get waveform
"""

from datetime import datetime as dt
from time import struct_time
from typing import Self

from . import oscilloscope

class MSO2014x(oscilloscope.Oscilloscope):
    """
    Class containing interface for the Tektronix MSO2014(B).
    Inherits from bench.Oscilloscope.
    """

    def __init__(self, address: str) -> None:
        """
        Constructor for the Oscilloscope class; connects to oscilloscope at {address}

        Arguments:
            address -- target oscilloscope's VISA address
        """

        super().__init__(address)  # call parent class constructor

        # set no header option
        self.write("header off")

        # set the date and time
        time: struct_time = dt.now().timetuple()
        self.write(f"date {time[0]}, {time[1]}, {time[2]}")
        self.write(f"time {time[3]}, {time[4]}, {time[5]}")

        # units the oscilloscope supports
        self.units = [
                "%", "/Hz", "A", "A/A", "A/V", "A/W", "A/dB", "A/s", "AA", "AW", "AdB",
                "As", "B", "Hz", "IRE", "S/s", "V", "V/A", "V/V", "V/W", "V/dB", "V/s",
                "VV", "VW", "VdB", "Volts", "Vs", "W", "W/A", "W/V", "W/W", "W/dB",
                "W/s", "WA", "WV", "WW", "WdB", "Ws", "dB", "dB/A", "dB/V", "dB/W",
                "dB/dB", "dBA", "dBV", "dBW", "dBdB", "day", "degrees", "div", "hr",
                "min", "ohms", "percent", "s"
                ] # programmers guide p.2-359

        print("INSTRUMENT INITIALIZED")

    def __get_channels(self, max: int = 8) -> int:
        settings = self.query("SET?")
        chan = []
        for i in range(max + 1): # check from 0 to max channels
            if f"CH{i}" in settings.upper():
                chan.append(i)
        return chan

    def __lock(self) -> Self:
        """
        Disable front panel controls
        """

        self.write("lock")  # disable front panel controls
        return self

    def __unlock(self) -> Self:
        """
        Enable front panel controls
        """

        self.write("unlock")  # disable front panel controls
        return self

    def __set_label(self, channel: int, label: str) -> Self:
        """
        Writes waveform labels to the oscilloscope screen

        Arguments:
            text -- label text, written to oscilloscope screen
            channel -- desired channel to label
        """

        self.write(f"ch{channel}:label \"{label}\"") # label it
        return self

    def __autoscale(self) -> Self:
        """
        Autoscales current channel
        """

        self.write("autoset enable")
        return self

    # Set Input Waveform Parameters

    def __set_input_n_bits(self, n_bits: int) -> Self:
        """
        
        """
        if n_bits in (8, 16):
            self.write(f"wfminpre:bit_nr {n_bits}")
        else:
            raise Exception("Bit Number Error: Only 8-bit and 16-bit allowed")
        return self

    def __set_input_binary_format(self, binary_format: str) -> Self:
        """
    
        """
        if binary_format.lower() == "unsigned":
            binary_format = "RP"
        else:
            binary_format = "RI"
        self.write(f"wfminpre:bn_fmt {binary_format}")
        return self

    def __set_input_n_bytes(self, n_bytes: int) -> Self:
        """
    
        """
        if n_bytes in (1, 2):
            self.write(f"wfminpre:byt_nr {n_bytes}")
        else:
            raise Exception("Byte Number Error: Only 1-byte and 2-byte allowed")
        return self

    def __set_input_byte_order(self, byte_order: str) -> Self:
        """
    
        """
        if byte_order in ("lsb", "msb"):
            self.write(f"wfminpre:byt_or {byte_order}")
        else:
            raise Exception("Byte Order Error: Only lsb (least-significant-byte) and msb (most-significant-byte) allowed")
        return self

    def __set_input_composition(self, composition: str) -> Self:
        """
    
        """
        if composition in ("composite_yt", "composite_env", "singular_yt"):
            self.write(f"wfminpre:composition {composition}")
        else:
            raise Exception("Composition Error: Only composite_yt, composite_env, and singular_yt allowed")
        return self

    def __set_input_encoding(self, encoding: str) ->  Self:
        """
    
        """
        if encoding in ("ascii", "binary"):
            self.write(f"wfminpre:encdg {encoding}")
        else:
            raise Exception("Encoding Error: Only ascii and binary encodings are allowed")
        return self

    def __set_input_filter_frequency(self, frequency: int) -> Self:
        """
    
        """ # does this really take an int?
        if frequency: # TODO check range of allowed frequencies
            self.write(f"wfminpre:filterfreq {frequency}")
        else:
            raise Exception("Filter Frequency Error: Invalid frequency selected")
        return self

    def __set_input_n_points(self, number: int) -> Self:
        """
    
        """
        self.write(f"wfminpre:nr_pt {number}")
        return self

    def __set_input_point_format(self, format: str) -> Self:
        """
    
        """
        if format in ("envelope", "singular"):
            self.write(f"wfminpre:encdg {format}")
        else:
            raise Exception("Encoding Error: Only ascii and binary encodings are allowed")
        return self

    def __set_point_offset(self, offset: int) -> Self:
        """
    
        """
        if offset: # unused
            self.write(f"wfminpre:pt_off {offset}")
        return self

    def __set_x_increment(self, increment: float) -> Self:
        """
    
        """
        self.write(f"wfminpre:xincr {increment}")
        return self

    def __set_x_unit(self, unit: str) -> Self:
        """
    
        """
        if unit in self.units:
            self.write(f"wfminpre:xunit {unit}")
        else:
            raise Exception("Unit Error: invalid unit")

    def __set_x_zero(self, zero: float) -> Self:
        """
    
        """
        self.write(f"wfminpre:xzero {zero}")
        return self

    def __set_y_multiplier(self, multiplier: float) -> Self:
        """
    
        """
        self.write(f"wfminpre:ymult {multiplier}")
        return self

    def __set_y_offset(self, offset: float) -> Self:
        """
    
        """
        self.write(f"wfminpre:ymult {offset}")
        return self

    def __set_y_unit(self, unit: str) -> Self:
        """
    
        """
        if unit in self.units:
            self.write(f"wfminpre:yunit {unit}")
        else:
            raise Exception("Unit Error: invalid unit")

    def __set_y_zero(self, zero: float) -> Self:
        """
    
        """
        self.write(f"wfminpre:yzero {zero}")
        return self

    # Get Input Waveform Parameters

    def __get_input_n_bits(self) -> int:
        """
        Gets the number of bits for waveform data - 8-bit or 16-bit
        
        Returns:
        """

        return self.query("wfminpre:bit_nr?")

    def __get_input_binary_format(self) -> str:
        """
        Gets the binary format for waveform data - signed or unsigned integer
        
        Returns:
        """

        return self.query("wfminpre:bn_fmt?")

    def __get_input_n_bytes(self) -> int:
        """
        Gets the number of bytes for waveform data - 1-byte or 2-byte
        
        Returns:
        """

        return self.query("wfminpre:byt_nr?")

    def __get_input_byte_order(self) -> str:
        """
        Gets the byte order for waveform data - least-significant-byte or most-significant-byte
        
        Returns:
        """

        return self.query("wfminpre:byt_or?")

    def __get_input_composition(self) -> str:
        """
        Gets the type of waveform data to be transferred
        
        Returns:
        """

        return self.query("wfminpre:composition?")

    def __get_input_encoding(self) -> str:
        """
        Gets the encoding for the waveform data - either ascii or binary
        
        Returns:
        """

        return self.query("wfminpre:encdg?")

    def __get_input_filter_frequency(self) -> float:
        """
        Gets the digital filter frequency for the waveform data
        
        Returns:
        """

        return self.query("wfminpre:filterfreq?")

    def __get_input_n_points(self) -> int:
        """
        Gets the number of points to acquire
        
        Returns:
        """

        return self.query("wfminpre:nr_pt?")

    def __get_input_point_format(self) -> str:
        """
        Gets the point format - envelope or singular
        
        Returns:
        """

        return self.query("wfminpre:pt_fmt?")

    def __get_input_point_offset(self) -> int:
        """
        Gets the point offset - unsused
        
        Returns:
        """

        return self.query("wfminpre:pt_off?")

    def __get_input_x_increment(self) -> float:
        """

        Gets the x increment, measured in units of x_unit
        
        Returns:
        """

        return self.query("wfminpre:xincr?")

    def __get_input_x_unit(self) -> str:
        """
        Gets the x unit for the waveform data
        
        Returns:
        """

        return self.query("wfminpre:xunit?")

    def __get_input_x_zero(self) -> float:
        """
        Gets the position value in x_unit of the first sample of the incoming waveform
        
        Returns:
        """

        return self.query("wfminpre:xzero?")

    def __get_input_y_multiplier(self) -> float:
        """
        Gets the vertical scale factor for the waveform data
        
        Returns:
        """

        return self.query("wfminpre:ymult?")

    def __get_input_y_offset(self) -> float:
        """
        Gets the vertical offset for the waveform data
        
        Returns:
        """

        return self.query("wfminpre:yoff?")

    def __get_input_y_unit(self) -> str:
        """    
        Gets the y_unit from the waveform input preamble
        
        Arguments: 
            None
        
        Returns: y unit string
        """

        return self.query("wfminpre:yunit?")

    def __get_input_y_zero(self) -> float:
        """
        Gets the y_zero value from the waveform input preamble
        
        Arguments:
            None
        
        Returns: y value, in units of y_unit, of the first data point
        """

        return self.query("wfminpre:yzero?")

    # Get Output Waveform Parameters

    def __get_output_n_bits(self) -> int:
        """
        Gets the number of bits for waveform data - 8-bit or 16-bit
        
        Returns:
        """

        return self.query("wfmoutpre:bit_nr?")

    def __get_output_binary_format(self) -> str:
        """
        Gets the binary format for waveform data - signed or unsigned integer
        
        Returns:
        """

        return self.query("wfmoutpre:bn_fmt?")

    def __get_output_n_bytes(self) -> int:
        """
        Gets the number of bytes for waveform data - 1-byte or 2-byte
        
        Returns:
        """

        return self.query("wfmoutpre:byt_nr?")

    def __get_output_byte_order(self) -> str:
        """
        Gets the byte order for waveform data - least-significant-byte or most-significant-byte
        
        Returns:
        """

        return self.query("wfmoutpre:byt_or?")

    def __get_output_composition(self) -> str:
        """
        Gets the type of waveform data to be transferred
        
        Returns:
        """

        return self.query("wfmoutpre:composition?")

    def __get_output_encoding(self) -> str:
        """
        Gets the encoding for the waveform data - either ascii or binary
        
        Returns:
        """

        return self.query("wfmoutpre:encdg?")

    def __get_output_filter_frequency(self) -> float:
        """
        Gets the digital filter frequency for the waveform data
        
        Returns:
        """

        return self.query("wfmoutpre:filterfreq?")

    def __get_output_n_points(self) -> int:
        """
        Gets the number of points to acquire
        
        Returns:
        """

        return self.query("wfmoutpre:nr_pt?")

    def __get_output_point_format(self) -> str:
        """
        Gets the point format - envelope or singular
        
        Returns:
        """

        return self.query("wfmoutpre:pt_fmt?")

    def __get_output_point_offset(self) -> int:
        """
        Gets the point offset - unsused
        
        Returns:
        """

        return self.query("wfmoutpre:pt_off?")

    def __get_output_x_increment(self) -> float:
        """

        Gets the x increment, measured in units of x_unit
        
        Returns:
        """

        return self.query("wfmoutpre:xincr?")

    def __get_output_x_unit(self) -> str:
        """
        Gets the x unit for the waveform data
        
        Returns:
        """

        return self.query("wfmoutpre:xunit?")

    def __get_output_x_zero(self) -> float:
        """
        Gets the position value in x_unit of the first sample of the incoming waveform
        
        Returns:
        """

        return self.query("wfmoutpre:xzero?")

    def __get_output_y_multiplier(self) -> float:
        """
        Gets the vertical scale factor for the waveform data
        
        Returns:
        """

        return self.query("wfmoutpre:ymult?")

    def __get_output_y_offset(self) -> float:
        """
        Gets the vertical offset for the waveform data
        
        Returns:
        """

        return self.query("wfmoutpre:yoff?")

    def __get_output_y_unit(self) -> str:
        """    
        Gets the y_unit from the waveform output preamble
        
        Arguments: 
            None
        
        Returns: y unit string
        """

        return self.query("wfmoutpre:yunit?")

    def __get_output_y_zero(self) -> float:
        """
        Gets the y_zero value from the waveform output preamble
        
        Arguments:
            None
        
        Returns: y value, in units of y_unit, of the first data point
        """

        return self.query("wfmoutpre:yzero?")

    def set_trigger(self, trigger_type: str, **kwargs) -> Self:
        """
        Sets the oscilloscope trigger, trigger type, and trigger parameters. 
        Most (all?) scopes have several triggering types.
        
        Positional Arguments:
            trigger_type        type of trigger used - edge_trigger, logic_trigger, etc.

        Keyword Arguments:
            trigger_level       vertical value to trigger waveform capture
            slope               'rise' or 'fall'; slope for various triggers
            coupling            'ac' or 'dc'; coupling mode for oscilloscope channel
            clock_source        one of the oscilloscope's channels - CHx, Dx, etc.
            when                logical pattern to trigger on when clock_source=none
            delta_time          time for logic pattern to hold when clock_source='none'
            clock_threshold     vertical value to trigger waveform capture for clock channel
            data_threshold      vertical value to trigger waveform capture for clock channel
            setup_time          time required for setup phase in setup and hold trigger
            hold_time           time required for hold phase in setup and hold trigger
            upper_threshold     upper threshold per channel, only used for runt and slew rate

        Returns:
            Self
        """

        # Trigger Setup
        if 'trigger_type' in kwargs:
            if trigger_type not in ('edge', 'pulse_width', 'logic', 'video', 'runt',
                                'transition', 'setup_and_hold', 'bus'):

                raise ValueError(f"MSO2014x does not support { trigger_type } as a trigger type")
        else:
            trigger_type = "edge" # edge trigger by default

        if "trigger_source" in kwargs and kwargs.get("trigger_source") in self.channels:
            trigger_source = kwargs.get("trigger_source")
        else:
            trigger_source = self.current_channel

        # Edge Trigger
        if trigger_type == "edge":

            self.write("trigger:a:type edge")
            self.write(f"trigger:a:edge:source ch{ trigger_source }")

            # Process Keyword Arguments
            if "trigger_level" in kwargs:
                self.write(f"trigger:a:level:{trigger_source} { kwargs.get('trigger_level') }" )
            else:
                raise ValueError(
                        "MSO2014x requires 'trigger_level' for edge triggering"
                        )

            if 'slope' in kwargs:
                self.write(f"trigger:a:edge:slope { kwargs.get('slope') }" ) # 'rise' or 'fall'
            else:
                self.write("trigger:a:edge:slope rise") # trigger on rise by default

            if 'coupling' in kwargs:
                self.write(f"trigger:a:edge:coupling { kwargs.get('coupling') }" )
            else:
                self.write(f"trigger:a:edge:coupling { self.__get_input_coupling() }" )

        # Logic Trigger
        if trigger_type == "logic":

            self.write("trigger:a:type logic")
            self.write("trigger:a:logic:class logic")

            # Check for clock_source
            if "clock_source" in kwargs and kwargs.get("clock_source") in self.channels:
                clock_source = kwargs.get("clock_source")
                self.write(f"trigger:a:logic:input:clock:source {clock_source}") # set clock source
            else:
                raise ValueError(
                        "MSO2014x requires 'clock_source' for logic triggering - 'none' is allowed"
                        )

            if "function" in kwargs and kwargs.get("function") in ("and", "nand"):
                self.write(f"trigger:a:logic:function { kwargs.get('function') } ")
            else:
                self.write("trigger:a:logic:function and")

            # Two main logic trigger types
            if clock_source == 'none': # trigger on logical pattern from channels

                if "when" in kwargs:
                    self.write(f"trigger:a:logic:pattern:when { kwargs.get('when') }" )
                else:
                    raise ValueError(
                            "MSO2014x requires 'when' to specify channels to trigger on pattern"
                            )

                if "delta_time" in kwargs:
                    self.write(f"trigger:a:logic:pattern:deltatime { kwargs.get('delta_time') }" )
                else:
                    raise ValueError(
                            "MSO2014x requires 'delta_time' to specify pattern hold time"
                            ) # check this, is it true?

            else: # trigger on pattern based on clock transition from channels

                if "slope" in kwargs:
                    self.write(f"trigger:a:logic:input:clock:edge { kwargs.get('slope') }" )
                else:
                    self.write("trigger:a:logic:input:clock:edge rise") # rising edge by default

                if "logic_input" in kwargs: # does logic:function go here?
                    self.write(f"trigger:a:logic:input:{ kwargs.get('logic_input') }" ) # set input
                else:
                    raise ValueError("MSO2014x requires logic_input for logic trigger")

        # Setup and Hold Trigger
        if trigger_type == "setup_and_hold":

            self.write("trigger:a:type logic")
            self.write("trigger:a:logic:class sethold")

            # Check for clock_source
            if "clock_source" in kwargs and kwargs.get("clock_source") in self.channels:
                clock_source = kwargs.get("clock_source")
                self.write(f"trigger:a:sethold:clock:source { clock_source }") # set clock source
            else:
                raise ValueError(
                        "MSO2014x requires 'clock_source' for setup and hold triggering"
                        )

            if "logic_input" in kwargs: # set input
                self.write(f"trigger:a:sethold:data:source { kwargs.get('logic_input') }" )
            else:
                raise ValueError("MSO2014x requires logic_input for setup and hold trigger")

            if 'slope' in kwargs: # 'rise' or 'fall'
                self.write(f"trigger:a:sethold:clock:edge { kwargs.get('slope') }" )
            else:
                self.write("trigger:a:edge:slope rise") # trigger on rise by default

            if "clock_threshold" in kwargs:
                self.write(f"trigger:a:sethold:clock:threshold { kwargs.get('clock_threshold') }" )
            else:
                self.write("trigger:a:sethold:clock:threshold ttl") # ttl level by default

            if "data_threshold" in kwargs: # data channels
                self.write(f"trigger:a:sethold:data:threshold { kwargs.get('data_threshold') }" )
            else:
                self.write("trigger:a:sethold:data:threshold ttl") # ttl level by default

            if "hold_time" in kwargs:
                self.write(f"trigger:a:sethold:holdtime { kwargs.get('hold_time') }" )
            else:
                raise ValueError("MSO2014x requires hold_time for setup and hold trigger")

            if "setup_time" in kwargs:
                self.write(f"trigger:a:sethold:setuptime { kwargs.get('setup_time') }" )
            else:
                raise ValueError("MSO2014x requires setup_time for setup and hold trigger")

            if "trigger_level" in kwargs:
                self.write(f"trigger:a:sethold:threshold { kwargs.get('trigger_level') }" )
            else:
                self.write("trigger:a:sethold:threshold ttl")

        # Pulse Width Trigger
            self.write("trigger:a:type pulse")
            self.write("trigger:a:pulse:class width")

            self.write(f"trigger:a:pulsewidth:source { trigger_source }")

            if "when" in kwargs:
                self.write(f"trigger:a:pulsewidth:when { kwargs.get('when') }" )
            else:
                raise ValueError("MSO2014x requires 'when' for pulse width triggering")

            if "width" in kwargs:
                self.write(f"trigger:a:pulsewidth:width { kwargs.get('width') }" )
            else:
                raise ValueError("MSO2014x requires 'width' for pulse width triggering")

            if "polarity" in kwargs:
                self.write( f"trigger:a:pulsewidth:polarity { kwargs.get('polarity') }" )
            else:
                self.write( "trigger:a:pulsewidth:polarity positive" ) # positive by default

        # Runt Trigger
        if trigger_type == "runt":
            self.write("trigger:a:type pulse")
            self.write("trigger:a:pulse:class runt")

            self.write("trigger:a:runt:source { trigger_source }")

            if "when" in kwargs:
                self.write(f"trigger:a:runt:when { kwargs.get('when') }" )
            else:
                raise ValueError("MSO2014x requires 'when' for runt triggering")

            if "width" in kwargs:
                self.write(f"trigger:a:runt:width { kwargs.get('width') }" )
            else:
                raise ValueError("MSO2014x requires 'width' for runt triggering")

            if "polarity" in kwargs:
                self.write( f"trigger:a:runt:polarity { kwargs.get('polarity') }" )
            else:
                self.write( "trigger:a:runt:polarity positive" ) # positive by default

            if "upper_threshold" in kwargs:
                # may want to change this from "current channel" to pass channel in as a kwarg
                self.write(f"trigger:a:upperthreshold:{ self.current_channel } { kwargs.get('upper_threshold') }")
