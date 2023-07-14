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


class DSOX120x(bench.Instrument):
    """
   Class containing interface for oscilloscope instruments. Currently supports Keysight DSOX1204G.

    Parent Class:
        Instrument
    """

    current_channel: int = 1  # initialize to channel 1
    num_channels: int = 4  # pull this from the instrument
    channel_list: list[int] = list(range(1, num_channels+1))

    def __init__(self, address) -> None:
        """
        Constructor for the Oscilloscope class; connects to oscilloscope at {address}

        Arguments:
            address -- target oscilloscope's VISA address
        """

        bench.Instrument.__init__(
            self, address)  # call parent class constructor for basic init

        # set the date and time
        time: struct_time = dt.now().timetuple()
        date_string: str = f"{time[0]}, {time[1]}, {time[2]}"
        time_string: str = f"{time[3]}, {time[4]}, {time[5]}"

        date_message: str = f"system:date {date_string}"
        time_message: str = f"system:time {time_string}"

        self.write(date_message)
        self.write(time_message)

        print("INSTRUMENT INITIALIZED")  # write initialization message

    def system_lock(self) -> None:
        """
        Disable front panel controls
        """

        message: str = f"system:lock on"
        self.write(message)  # disable front panel controls

    def system_unlock(self) -> None:
        """
        Enable front panel controls
        """

        message: str = f"system:lock off"
        self.write(message)  # disable front panel controls

    def channel(self, channel_number) -> Self | None:
        """
        sets the oscilloscope channel to operate on

        Arguments:
            channel_number -- number of channel to select

        Returns:
            self - returns parent object for second method call
        """

        match channel_number:

            case "":
                pass

            case chan if chan in self.channel_list:  # if a real channel is selected,
                self.current_channel = channel_number # set current_channel to selected channel
                return self  # return instance

            case _:  # otherwise return an error message
                pass

    def set_label(self, channel, label) -> None:
        """
        Writes waveform labels to the oscilloscope screen

        Arguments:
            text -- label text, written to oscilloscope screen
            channel -- desired channel to label
        """
        # there are two sections to each message here, the command and the label itself
        # the command section is the one that varies, so the label code can stay the same each time

        if not label: # if there is no label provided, make one up
            label = "Channel {channel}"
        label = f"\"{label}\"" # we need the label to be surrounded by escaped double-quotes
        
        # the instrument itself requires specific commands
        command: str = f"channel{channel}:label "

        match channel:
            case chan if chan in self.channel_list:  # if a real channel is selected,
                self.write(command + label) # label it
            case _:  # otherwise return an error message
                pass

        # write the label(s) to the oscilloscope screen
        self.write("display:label on")  # show the label

        return self

    def autoscale(self) -> None:
        """
        Autoscales current channel
        """
        
        message: str = f"autoscale channel{self.current_channel}"
        self.write(message)

    def get_waveform(self) -> tuple[list[float], list[float]]:
        """
        Pulls displayed waveform data from the connected oscilloscope without changing
        any settings

        Returns:
            t       -- list of conditioned x-axis data from oscilloscope acquisition
            x       -- list of conditioned y-axis data from oscilloscope acquisition
        """

        # set oscilloscope to save measurement sample
        self.write("waveform:points:mode normal")

        # max number of points - play around with this
        self.write("waveform:points 1000")

        # output in formatted ascii floating point
        self.write("waveform:format ascii")

        self.write(f"waveform:source channel{self.current_channel}")

        waveform_preamble: list[str] = self.query(
            "waveform:preamble?").split(',')  # get the preamble

        # 0=byte, 1=word, 4=ascii
        # waveform_format: int = int(waveform_preamble[0])

        # 0=normal, 1=peak detect, 2=average
        # waveform_type: int = int(waveform_preamble[1])

        # number of data points transferred
        # waveform_points = int(waveform_preamble[2])

        # waveform_count: bool = bool(waveform_preamble[3])  # always equal to 1

        # time difference between datapoints
        t_increment: float = float(waveform_preamble[4])

        # always first data point in memory
        # t_origin: float = float(waveform_preamble[5])

        # value associated with x_origin
        # t_reference: float = float(waveform_preamble[6])

        # voltage difference between points
        # x_increment: float = float(waveform_preamble[7])

        # voltage at center screen
        # x_origin: float = float(waveform_preamble[8])

        # value where y-origin occurs
        # x_reference: float = float(waveform_preamble[9])

        # pull waveform from memory
        x_raw: str = self.query("waveform:data?")

        # remove the ascii header and cast to float
        x_data: list[float] = [float(x) for x in x_raw.split(',')[1:]]

        # generate time vector
        t_data: list[float] = [t_increment*t for t in range(0, len(x_data))]

        return t_data, x_data

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
