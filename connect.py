#!/usr/bin/env python
"""Short script to list connect instruments."""

from bench import InstrumentFinder

finder = InstrumentFinder()
instruments = finder.find_instruments()
info = finder.get_info(instruments)
print(info)
