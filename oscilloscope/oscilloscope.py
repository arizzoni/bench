#!/usr/bin/env python3.11
"""
bench/oscilloscope/oscilloscope.py - Oscilloscope class for the bench module

TODO
Trigger
    
Display
    Label
    Clear
Channel
    Attenuation
    Coupling Impedance Signal Type
    BW Limit
Waveform
    Vertical Range
    Horizontal Timebase
    Offset
    Waveform Inversion
Measure
"""

from abc import ABC, abstractmethod
from typing import Self

from .. import bench

class Oscilloscope(bench.Instrument, ABC):
    """
    Class containing interface for oscilloscopes.
    Inherits from bench.Instrument. Abstract base class, should not be 
    instantiated on it's own.
    """

    def __init__(self, address: str) -> None:
        """
        Constructor for the Oscilloscope class; connects to oscilloscope at
        {address}

        Arguments:
            address -- target oscilloscope's VISA address
        """

        super().__init__(address)  # call parent class constructor for basic init

        self.channels: list(int) = self.get_channels() # Returns array of channel numbers
        self.current_channel = 1

    def __subclasshook__(self) -> True or False or NotImplemented:
        """
        TODO: Test if a class is a subclass of Oscilloscope.
        """
        return NotImplemented


    def channel(self, channel_number: int) -> Self | None: # move to instrument
        """
        sets the oscilloscope channel to operate on

        Arguments:
            channel_number -- number of channel to select

        Returns:
            self - returns parent object for second method call
        """

        if channel_number in self.channels:
            self.current_channel = channel_number # set current_channel
        else:
            raise ValueError("Channel Number Error: Channel out of range")

        return self  # return instance


    def get_input_parameters(self) -> Self:
        """
        Gets the parameters for the waveform prior to acquisition and returns a
        list
        
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

        return [
                self.get_input_n_bits(),
                self.get_input_binary_format(),
                self.get_input_n_bytes(),
                self.get_input_byte_order(),
                self.get_input_composition(),
                self.get_input_encoding(),
                self.get_input_filter_frequency(),
                self.get_input_n_points(),
                self.get_input_point_format(),
                self.get_input_point_offset(),
                self.get_input_x_increment(),
                self.get_input_x_unit(),
                self.get_input_x_zero(),
                self.get_input_y_multiplier(),
                self.get_input_y_offset(),
                self.get_input_y_unit(),
                self.get_input_y_zero()
                ]


    def get_output_parameters(self) -> Self: # move to oscilloscope
        """
        Gets the parameters for the waveform prior to acquisition and returns a
        list
        
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

        return [
                self.get_output_n_bits(),
                self.get_output_binary_format(),
                self.get_output_n_bytes(),
                self.get_output_byte_order(),
                self.get_output_composition(),
                self.get_output_encoding(),
                self.get_output_filter_frequency(),
                self.get_output_n_points(),
                self.get_output_point_format(),
                self.get_output_point_offset(),
                self.get_output_x_increment(),
                self.get_output_x_unit(),
                self.get_output_x_zero(),
                self.get_output_y_multiplier(),
                self.get_output_y_offset(),
                self.get_output_y_unit(),
                self.get_output_y_zero()
                ]


    @abstractmethod
    def lock(self) -> Self: # move to instrument
        """
        Disable the instrument's front panel controls.
        """


    @abstractmethod
    def unlock(self) -> Self: # move to instrument
        """
        Enable the instrument's front panel controls.
        """


    @abstractmethod
    def set_label(self, label: str) -> Self:
        """
        Writes waveform labels to the oscilloscope screen for the current
        channel.

        Arguments:
            label -- label text, written to oscilloscope screen
        """


    @abstractmethod
    def autoscale(self) -> Self:
        """
        Send built-in autoscale command to the instrument. Note that different
        scopes may implement different behavior. It may be beneficial to define
        the desired behavior explicitly using other commands.
        """


    @abstractmethod
    def get_channels(self) -> Self:
        """
        Returns the number of channels the current instrument supports.
        """


    @abstractmethod
    def get_input_n_bits(self) -> int:
        """
        Gets the number of bits per binary waveform point for the
        incoming waveform.
        """


    @abstractmethod
    def get_input_binary_format(self) -> int:
        """
        Gets the format of binary data for the incoming waveform. Signed
        integer (RI) or positive/unsigned integer (RP).
        """


    @abstractmethod
    def get_input_n_bytes(self) -> int:
        """
        
        """


    @abstractmethod
    def get_input_byte_order(self) -> int:
        """
        
        """


    @abstractmethod
    def get_input_composition(self) -> int:
        """
        Returns the type of data the QUERY command will give.
        """


    @abstractmethod
    def get_input_encoding(self) -> int:
        """
        
        """


    @abstractmethod
    def get_input_filter_frequency(self) -> int:
        """
        Returns the cutoff frequency of the oscilloscope channel's input filter.
        """


    @abstractmethod
    def get_input_n_points(self) -> int:
        """
        Returns the number of data points in the waveform data input buffer.
        """


    @abstractmethod
    def get_input_point_format(self) -> int:
        """
        Returns the format of the data points in the waveform data input buffer.
        """


    @abstractmethod
    def get_input_point_offset(self) -> int:
        """
        Returns x-offset of data points in the waveform data input buffer.
        """


    @abstractmethod
    def get_input_x_increment(self) -> int:
        """
        Returns x-scale of the waveform data.
        """


    @abstractmethod
    def get_input_x_unit(self) -> int:
        """
        Returns x-unit of the waveform data.
        """


    @abstractmethod
    def get_input_x_zero(self) -> int:
        """

        """


    @abstractmethod
    def get_input_y_multiplier(self) -> int:
        """

        """


    @abstractmethod
    def get_input_y_offset(self) -> int:
        """

        """


    @abstractmethod
    def get_input_y_unit(self) -> int:
        """

        """


    @abstractmethod
    def get_input_y_zero(self) -> int:
        """

        """


    @abstractmethod
    def get_output_n_bits(self) -> int:
        """

        """


    @abstractmethod
    def get_output_binary_format(self) -> int:
        """

        """


    @abstractmethod
    def get_output_n_bytes(self) -> int:
        """

        """


    @abstractmethod
    def get_output_byte_order(self) -> int:
        """

        """


    @abstractmethod
    def get_output_composition(self) -> int:
        """

        """


    @abstractmethod
    def get_output_encoding(self) -> int:
        """

        """


    @abstractmethod
    def get_output_filter_frequency(self) -> int:
        """

        """


    @abstractmethod
    def get_output_n_points(self) -> int:
        """

        """


    @abstractmethod
    def get_output_point_format(self) -> int:
        """

        """


    @abstractmethod
    def get_output_point_offset(self) -> int:
        """

        """


    @abstractmethod
    def get_output_x_increment(self) -> int:
        """

        """


    @abstractmethod
    def get_output_x_unit(self) -> int:
        """

        """


    @abstractmethod
    def get_output_x_zero(self) -> int:
        """

        """


    @abstractmethod
    def get_output_y_multiplier(self) -> int:
        """

        """


    @abstractmethod
    def get_output_y_offset(self) -> int:
        """

        """


    @abstractmethod
    def get_output_y_unit(self) -> int:
        """

        """


    @abstractmethod
    def get_output_y_zero(self) -> int:
        """

        """


    @abstractmethod
    def set_input_binary_format(self) -> int:
        """

        """


    @abstractmethod
    def set_input_n_bytes(self) -> int:
        """

        """


    @abstractmethod
    def set_input_byte_order(self) -> int:
        """

        """


    @abstractmethod
    def set_input_composition(self) -> int:
        """

        """


    @abstractmethod
    def set_input_encoding(self) -> int:
        """

        """


    @abstractmethod
    def set_input_filter_frequency(self) -> int:
        """

        """


    @abstractmethod
    def set_input_n_points(self) -> int:
        """

        """


    @abstractmethod
    def set_input_point_format(self) -> int:
        """

        """


    @abstractmethod
    def set_input_point_offset(self) -> int:
        """

        """


    @abstractmethod
    def set_input_x_increment(self) -> int:
        """

        """


    @abstractmethod
    def set_input_x_unit(self) -> int:
        """

        """


    @abstractmethod
    def set_input_x_zero(self) -> int:
        """

        """


    @abstractmethod
    def set_input_y_multiplier(self) -> int:
        """

        """


    @abstractmethod
    def set_input_y_offset(self) -> int:
        """

        """


    @abstractmethod
    def set_input_y_unit(self) -> int:
        """

        """


    @abstractmethod
    def set_input_y_zero(self) -> int:
        """

        """


    @abstractmethod
    def set_trigger_parameters(self):
        """

        """


    @abstractmethod
    def get_trigger_parameters(self):
        """

        """


    @abstractmethod
    def trigger(self): # TODO
        """

        """


    @abstractmethod
    def set_input_attenuation(self):
        """

        """


    @abstractmethod
    def get_input_attenuation(self):
        """

        """


    @abstractmethod
    def set_input_coupling(self):
        """

        """


    @abstractmethod
    def get_input_coupling(self):
        """

        """


    @abstractmethod
    def set_input_impedance(self):
        """

        """


    @abstractmethod
    def get_input_impedance(self):
        """

        """


    @abstractmethod
    def set_signal_type(self):
        """

        """


    @abstractmethod
    def get_signal_type(self):
        """

        """


    @abstractmethod
    def set_acquisition_mode(self):
        """

        """


    @abstractmethod
    def get_acquisition_mode(self):
        """

        """


    @abstractmethod
    def set_horizontal_scale(self):
        """

        """


    @abstractmethod
    def get_horizontal_scale(self):
        """

        """


    @abstractmethod
    def set_vertical_scale(self):
        """

        """


    @abstractmethod
    def get_vertical_scale(self):
        """

        """


    @abstractmethod
    def get_waveform(self):
        """

        """
