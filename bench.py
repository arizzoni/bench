#!/usr/bin/env python3.11

from abc import ABC, abstractmethod
import pyvisa

class Instrument(ABC):
    """
    Instrument class containing basic IEEE-488 standard commands and a framework for basic
    instrument functionality.

    Methods:
        write()
        read()
        query()
        clear_status()
        set_ese()
        get_ese()
        get_info()
        reset()
        set_opc()
        get_opc()
    """

    def __init__(self, address: str) -> None:
        """
        Constructor for the Instrument class. Connects to instrument at {address}

        Arguments:
            address -- address of the instrument to connect to
        """
        self.address: str = address  # save address for later

        # start the resource manager
        self.resource_manager: pyvisa.ResourceManager = pyvisa.ResourceManager()

        # begin communicating with the instrument
        self.instrument: pyvisa.Resource = self.resource_manager.open_resource(
            self.address)

    def close(self) -> None:
        """Close the pyvisa Resource Manager session
        """
        self.resource_manager.close()

    def write(self, command: str) -> None:
        """
        Writes the passed command to the instrument
        Arguments:
            command -- command string to pass to the instrument
        """

        self.instrument.write(command)  # wrap the pyvisa write command

    def read(self) -> str:
        """
        Reads from the instrument and returns passed information

        Returns:
            returns string passed by instrument
        """

        return self.instrument.read()  # wrap the pyvisa read command

    def query(self, command: str) -> str:
        """
        queries instrument - equivalent to a write() immediately followed by a read()

        Arguments:
            command -- command string to pass to the instrument

        Returns:
            returns string passed by instrument
        """

        self.write(command)  # write to instrument
        return self.read()  # read from instrument

    def clear_status(self) -> None:
        """
        Clears the Status Byte register and all event registers
        """

        self.write("*cls")  # clear status and event registers

    def set_ese(self, bits) -> None:
        """
        Enables bits in the Standard Event Enable register. Selected bits are
        then reported to Status Byte.

        Arguments:
            bits -- bits to enable in the IEEE-488 Standard Event Enable register

        Standard Event Status Register:

        Bit 0: OPC: Operation Complete.

        Bit 1: unused: Always set to 0.

        Bit 2: QYE: Query Error. The power supply tried to read the output
        buffer but it was empty. Or, a new command line was received before a
        previous query had been read. Or, both the input and output buffers
        are full.

        Bit 3: DDE: Device Error. Self-test or calibration error occurred.

        Bit 4: EXE: Execution Error. An execution error occurred.

        Bit 5: CME: Command Error. A command syntax error occurred.

        Bit 6: unused: Always set to 0.

        Bit 7: PON: Power On. Power has been turned off and on since the last
        time the event register was read or cleared.
        """

        self.write(f"*ese {bits}")

    def get_ese(self, bits) -> str:
        """
        Queries bits in the Standard Event Enable register.
        Selected bits are then reported to Status Byte

        Arguments:
            bits -- bits to get in the IEEE-488 Standard Event Enable register

        Returns:
            returns callback for write function

        Standard Event Status Register:

        Bit 0: OPC: Operation Complete.

        Bit 1: unused: Always set to 0.

        Bit 2: QYE: Query Error. The power supply tried to read the output
        buffer but it was empty. Or, a new command line was received before a
        previous query had been read. Or, both the input and output buffers
        are full.

        Bit 3: DDE: Device Error. Self-test or calibration error occurred.

        Bit 4: EXE: Execution Error. An execution error occurred.

        Bit 5: CME: Command Error. A command syntax error occurred.

        Bit 6: unused: Always set to 0.

        Bit 7: PON: Power On. Power has been turned off and on since the last
        time the event register was read or cleared.
        """

        return self.query(f"*ese {bits}?")

    def get_info(self) -> str:
        """
        Gets instrument ID string: Manufacturer, Part Number, Serial Number, 
        and Software Revision


        Returns:
            returns instrument *idn response: manufacturer, mpn,
            serial number, and sw rev
        """

        return self.query("*idn?")

    def reset(self) -> None:
        """
        Reset instrument to factory settings
        """

        self.write("*rst")

    def set_opc(self) -> None:
        """
        Sets the Operation Complete bit in the instrument's Standard Event Register
        at the completion of the current operation.
        """

        self.write("*opc")

    def get_opc(self) -> str:
        """
        Gets the value of the Operation Complete bit from the Standard Event Register

        Returns:
            operation complete bit
        """

        return self.query("*opc?")


class InstrumentFinder():
    """
    This is a class to detect serial instruments using the VISA interface.

    TODO
    - add functionality to find_instruments
    - Error handling
    """

    def __init__(self) -> None:
        """
        Constructor for the InstrumentFinder class; starts resource manager
        """

        # start the resource manager at initialization
        self.resource_manager: pyvisa.ResourceManager = pyvisa.ResourceManager()

    def find_instruments(self) -> tuple[str, ...]:
        """
        Function to find and list connected serial devices
        TODO
        - Update to look for certain instrument types, prefer USB over LAN, etc.
            - Is is possible to identify the type of instrument and pull data e.g. num channels?
        """

        # generate a list of connected serial devices
        instruments: tuple[str, ...] = self.resource_manager.list_resources()

        # display count of connected devices
        print(f'{len(instruments)} DEVICES DETECTED:')

        return instruments

    def get_info(self, instruments) -> None:
        """Gets information about the detected instruments and prints it to console

        Arguments:
            instruments -- tuple of instruments found using find_instruments
        """
        # iterate through connected instruments to get describing information
        for instrument in instruments:

            info: tuple(str, ...) = self.resource_manager.open_resource(instrument).query(
                "*idn?").split(',')  # query instrument identifier information

            manufacturer: str = info[0]  # split out manufacturer
            model_number: str = info[1]  # split out model number
            serial_number: str = info[2]  # split out serial number
            revision_code: str = info[3]  # split out revision code

            # print the identifier information
            print(
                f"\n{manufacturer} {model_number}\n",
                f"SN: {serial_number}\nREV: {revision_code}\nADDRESS: {instrument}")
