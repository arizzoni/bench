#!/usr/bin/env python3.11
# bench/oscilloscope/oscilloscope.py - Oscilloscope class for the bench module

'''
_summary
'''
# TODO
# trigger
# vertical range
# horizontal timebase
# attenuation
# coupling
# offset
# waveform inversion 
# impedance 
# signal type
# bwlimit
# get waveform

from typing import Self

from .. import bench

class Oscilloscope(bench.Instrument):
    """
    Class containing interface for oscilloscopes.
    Inherits from bench.Instrument.
    """

    def __init__(self, address: str) -> None:
        """
        Constructor for the Oscilloscope class; connects to oscilloscope at
        {address}

        Arguments:
            address -- target oscilloscope's VISA address
        """

        bench.Instrument.__init__(
            self, address)  # call parent class constructor for basic init

        self.channels: int = self.__get_channels() # Returns array of channel numbers

    def lock(self) -> Self:
        """
        Disable front panel controls
        """

        self.__lock()  # disable front panel controls
        return self

    def unlock(self) -> Self:
        """
        Enable front panel controls
        """

        self.__unlock()  # disable front panel controls
        return self

    def channel(self, channel_number: int) -> Self | None:
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
            raise Exception("Channel Number Error: Channel out of range")
        return self  # return instance

    def set_label(self, label: str) -> Self:
        """
        Writes waveform labels to the oscilloscope screen

        Arguments:
            label -- label text, written to oscilloscope screen
        """

        self.__set_label(self.current_channel, label)
        return self

    def autoscale(self) -> Self:
        """
        Autoscales current channel
        """

        self.__autoscale()
        return self

    # Get Input Waveform Parameters

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
                self.__get_input_n_bits(), 
                self.__get_input_binary_format(), 
                self.__get_input_n_bytes(), 
                self.__get_input_byte_order(), 
                self.__get_input_composition(),
                self.__get_input_encoding(), 
                self.__get_input_filter_frequency(), 
                self.__get_input_n_points(),
                self.__get_input_point_format(),
                self.__get_input_point_offset(),
                self.__get_input_x_increment(),
                self.__get_input_x_unit(),
                self.__get_input_x_zero(),
                self.__get_input_y_multiplier(),
                self.__get_input_y_offset(),
                self.__get_input_y_unit(),
                self.__get_input_y_zero()
                ]

    # Get Output Waveform Parameters

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
                self.__get_output_n_bits(), 
                self.__get_output_binary_format(), 
                self.__get_output_n_bytes(), 
                self.__get_output_byte_order(), 
                self.__get_output_composition(),
                self.__get_output_encoding(), 
                self.__get_output_filter_frequency(), 
                self.__get_output_n_points(),
                self.__get_output_point_format(),
                self.__get_output_point_offset(),
                self.__get_output_x_increment(),
                self.__get_output_x_unit(),
                self.__get_output_x_zero(),
                self.__get_output_y_multiplier(),
                self.__get_output_y_offset(),
                self.__get_output_y_unit(),
                self.__get_output_y_zero()
                ]

    # Set Input Waveform Parameters

    def set_input_parameters(self, n_bits, binary_format, n_bytes, byte_order, composition,
                         encoding, frequency, n_points, point_format, point_offset,
                         x_increment, x_unit, x_zero, y_multiplier, y_offset, y_unit,
                         y_zero) -> Self:
        if n_bits:
            self.__set_input_n_bits(n_bits)
        if binary_format:
            self.__set_input_binary_format(format)
        if n_bytes:
            self.__set_input_n_bytes(n_bytes)
        if byte_order:
            self.__set_input_byte_order(byte_order)
        if composition:
            self.__set_input_composition(composition)
        if encoding:
            self.__set_input_encoding(encoding)
        if frequency:
            self.__set_input_filter_frequency(frequency)
        if n_points:
            self.__set_input_n_points(n_points)
        if point_format:
            self.__set_input_point_format(point_format)
        if point_offset:
            self.__set_input_point_offset(point_offset)
        if x_increment:
            self.__set_input_x_increment(x_increment)
        if x_unit:
            self.__set_input_x_unit(x_unit)
        if x_zero:
            self.__set_input_x_zero(x_zero)
        if y_multiplier:
            self.__set_input_y_multiplier(y_multiplier)
        if y_offset:
            self.__set_input_y_offset(y_offset)
        if y_unit:
            self.__set_input_y_unit(y_unit)
        if y_zero:
            self.__set_input_y_zero(y_zero)

# still need to write methods but have them raise this error instead
#   def methodB(self):
#       raise NotImplementedError("Must override methodB")
# stackoverflow.com/questions/25062114/calling-child-class-method-from-parent-class-file-in-python




# TODO

    def set_trigger_parameters(): #TODO
        return 0

    def get_trigger_parameters(): #TODO
        return 0

    def set_input_attenuation(): #TODO
        return 0

    def get_input_attenuation(): #TODO
        return 0

    def set_input_coupling(): #TODO
        return 0

    def get_input_coupling(): #TODO
        return 0

    def set_input_impedance(): #TODO
        return 0

    def get_input_impedance(): #TODO
        return 0

    def set_signal_type(): #TODO
        return 0

    def get_signal_type(): #TODO
        return 0

    def set_acquisition_mode(): #TODO
        return 0

    def get_acquisition_mode(): #TODO
        return 0

    def set_horizontal_scale(): #TODO
        return 0

    def get_horizontal_scale(): #TODO
        return 0

    def set_vertical_scale(): #TODO
        return 0

    def get_vertical_scale(): #TODO
        return 0

    def get_waveform(): #TODO
        return 0
