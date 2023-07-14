#!/usr/bin/env python3.11

"""_summary_

Returns:
    _description_
"""

from typing import Self

from .. import bench


class edu33210(bench.Instrument):
    """
    _summary_ # TODO

    Parent Class:
        Instrument
    """

    current_channel: int = 1  # initialize to channel 1

    num_channels: int = 2  # pull this from the instrument

    channel_list: list[int] = list(range(1, num_channels+1))

    def __init__(self, address) -> None:
        bench.Instrument.__init__(
            self, address)  # call parent class constructor for basic init

        print("INSTRUMENT INITIALIZED")  # write initialization message

    def channel(self, channel_number) -> Self | None:
        """
        Sets the function generator channel to operate on

        Arguments:
            channel_number -- number of channel to select

        Returns:
            self - returns parent object for second method call
        """ # TODO cleanup comments

        match channel_number:

            case "":
                pass

            case chan if chan in self.channel_list:  # if a real channel is selected, select it
                self.current_channel = channel_number
                return self  # return instance

            case _:  # otherwise return an error message
                pass

    def apply(self, function, frequency, amplitude, offset) -> None:
        """
        Set current channel to output selected waveform

        Arguments:
            function -- str: waveform: sinusoid, square, ramp, etc
            frequency -- float: waveform frequency
            amplitude -- float: waveform amplitude
            offset -- float: waveform dc component
        """
        
        self.write(
            f"apply:{function} {frequency},{amplitude},{offset}")

    def output_off(self) -> None:
        """Disable output connectors
        """
        self.write(f"output{self.current_channel} off")
        
    def set_output_load(self, load: float|str = "inf") -> None:
        """Set output termination. Should equal load impedance at the input.
           High impedance mode is the default.
        """
        self.write(f"output{self.current_channel}:load {load}")
        
    def get_output_load(self) -> str:
        """Gets output termination for the current channel.
        """
        return self.query(f"output{self.current_channel}:load?")
    
    def set_function(self, function: str) -> None:    
        """Sets the waveform function for the current channel. Options are: 
        sinusoid, square, triangle, ramp, pulse, prbs, noise, arb, dc
        """  
        self.write(f"source{self.current_channel}:function {function}")

    def get_function(self) -> str:    
        """Gets the waveform function for the current channel
        """  
        return self.query(f"source{self.current_channel}:function?")
        
    def get_frequency(self) -> None:
        """Gets the current channel's frequency setting
        """
        return self.query(f"source{self.current_channel}:frequency?")
    
    def set_frequency(self, frequency: float|list(float), dwell: float|list(float) = 1) -> None:
        """Sets the frequency or list of frequencies for the current channel. Note that different
        waveforms may have different maximum frequencies depending on the
        instrument.
        """              
                
            
        if len(frequency) == 1:
            self.write(f"source{self.current_channel}:frequency {frequency}")
        elif len(frequency) > 1:
            self.write(f"source{self.current_channel}:list:frequency {frequency}")
            self.write(f"source{self.current_channel}:list:dwell {dwell}")

    def set_sweep(self, start: float, stop: float, spacing: str = "log", time: float = 1e0) -> None:
        """Sets the frequency or list of frequencies for the current channel. Note that different
        waveforms may have different maximum frequencies depending on the
        instrument.
        """        
        self.write(f"source{self.current_channel}:frequency:start {start}")
        self.write(f"source{self.current_channel}:frequency:stop {stop}")
        self.write(f"source{self.current_channel}:sweep:spacing {spacing}")
        self.write(f"source{self.current_channel}:sweep:time {time}")
        
    def set_coupling(self, couple: bool = False, couple_mode: str = "ratio") -> None:
        """Sets inter-channel coupling state and mode. Ratio or offset.
        """
        self.write(f"source{self.current_channel}:frequency:couple {int(couple)}")
        self.write(f"source{self.current_channel}:frequency:couple:mode {couple_mode}")  