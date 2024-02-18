''' connect instruments '''
import pyvisa
import bench

finder = bench.InstrumentFinder()
instruments = finder.find_instruments()
info = finder.get_info(instruments)

