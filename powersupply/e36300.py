#!/usr/bin/env python3.11

"""_summary_

Returns:
    _description_
"""

from datetime import datetime as dt
from time import struct_time

from .. import bench


class E36300(bench.Instrument):
    """Class to interface with a bench power supply. Currently supports Keysight E36313A.

    Parent Class:
        Instrument
    """

    def __init__(self, address: str) -> None:
        """
        Constructor for the Power Supply class. Queries instruments to determine channel count,
        current and voltage settings, etc.

        Arguments:
            address -- VISA address of the instrument
        """

        bench.Instrument.__init__(
            self, address)  # call parent class constructor for basic init

        time: struct_time = dt.now().timetuple()
        self.write(f"system:date {time[0]}, {time[1]}, {time[2]}")
        self.write(f"system:time {time[3]}, {time[4]}, {time[5]}")

        # TODO
        # How can I pull this from the instrument automatically?

        self.num_channels: int = 3

        self.ch1_imax: int = 10
        self.ch1_vmax: int = 6
        self.ch2_imax: int = 2
        self.ch2_vmax: int = 25
        self.ch3_imax: int = 2
        self.ch3_vmax: int = 25

        self.imax: list[int] = [self.ch1_imax, self.ch2_imax, self.ch3_imax]
        self.vmax: list[int] = [self.ch1_vmax, self.ch2_vmax, self.ch3_vmax]

        print("INSTRUMENT INITIALIZED")  # instrument initialization complete

    def status(self):
        """
        Gets the status of the instrument. Includes:
            - Output State
            - Voltage/current settings
            - Event Registers TODO
            - Error Logs TODO
        """

        for channel in range(0, self.num_channels):  # iterate through the channels
            channel += 1
            self.write(   # select the current channel
                "instrument:select CH{channel}")

            output_state: str = self.query(
                "channel:output?").strip()  # query output state, remove leading and trailing spaces

            if output_state == "1":
                output_state_str: str = "ON"

            elif output_state == "0":
                output_state_str: str = "OFF"

            else:  # this could raise an exception
                output_state_str: str = "UNKNOWN"

            # print current channel for debug
            print(f"Channel {channel}")

            current_setting: float = float(self.query(
                "current?"))  # query OCP setting

            voltage_setting: float = float(self.query(
                "voltage?"))  # query voltage setting

            # print settings
            print(f"Voltage: {voltage_setting} V")
            print(f"Current: {current_setting} A")  # print OCP setting

            # print output status
            print(f"Output Status: {output_state_str}\n")

    def set(self, channel: int, voltage: float, current_limit: float) -> None:
        """
        Sets the power supply at the specified output (channel) with the specified voltage and
        specified current limit. If the desired setpoint is beyond the capabilities of the supply,
        raise an exception

        Arguments:
            channel -- channel to set
            voltage -- desired output voltage
            current_limit -- desired overcurrent protection threshold
        """

        self.write(
            f"apply ch{channel},{voltage},{current_limit}")

    def output_on(self, channel: int) -> None:
        """
        Turns on the output to the specified channel or channels

        Arguments:
            channel -- channel or channels to turn on
        """

        if channel == 'ALL' or channel is None:  # if no channel is specified, turn on all channels
            for channel in range(0, 3):  # iterate through channels
                channel += 1
                self.write(  # select channel
                    f"instrument:select ch{channel}")

                # turn on selected channel
                self.write("channel:output on")

        else:
            self.write(  # select channel
                f"instrument: select ch{channel}")

            # turn on selected channel
            self.write("output on")

    def output_off(self, channel: int) -> None:
        """Turns off the output to the specified channel or channels

        Arguments:
            channel -- channel or channels to turn off
        """

        if channel.upper == 'ALL' or channel is None:  # if no channel is specified, turn on all channels
            for channel in range(0, 3):
                channel += 1

                self.write(  # select channel
                    f"instrument:select ch{channel}")

                # turn on selected channel
                self.write("channel:output off")

        else:
            self.write(
                f"instrument:select ch{channel}")  # select channel

            # turn on selected channel
            self.write("channel:output off")

    def set_display_text(self, text) -> None:
        """Sets display text

        Arguments:
            text -- text to write to display
        """
        if text is not None:
            self.write(f"display:text \"{text}\"")
        else:
            self.write("display:text \"KEYSIGHT E36313A\"")

    def get_display_text(self) -> str:
        """Gets display text

        Returns:
            display text
        """
        text: str = self.query("display:text?")

        return text

    def get_display_state(self) -> bool:
        """_summary_

        Returns:
            _description_
        """
        display_status: bool = self.query("display?")

        return display_status

    def set_display_state(self, state: bool) -> None:
        """_summary_

        Arguments:
            state -- _description_
        """
        if state == True:
            self.write("display on")
        elif state == False:
            self.write("display off")
        else:
            pass  # TODO

    def display(self, text: str) -> None:
        """
        Writes text to the instrument display. To clear, write an empty string

        TODO
        - Should writing an empty string be how the screen is cleared?

        Arguments:
            text -- text to write to the instrument display. 30 char max
        """

        self.write(
            f"disp:text \"{text}\"")  # write {text} to screen. 30 char max

    def remote_only(self) -> None:
        """
        Disables front panel controls
        """

        self.write("system:remote")  # disable front panel controls
