from gpib_device import GPIBDevice

class FrequencyCounter(GPIBDevice):
    def __init__(self, gpib_device=0, gpib_address=3):
        super().__init__(gpib_device, gpib_address)
        idn_response = self.idn()
        assert idn_response[1] == '53131A'

    def measure_frequency(self, *, expected_frequency=None, resolution=None):
        cmd = 'MEAS:FREQ?'
        if expected_frequency is not None:
            cmd += f' {expected_frequency:e}Hz'
            if resolution is not None:
                cmd += f', {resolution}Hz'
        return float(self.query(cmd))

dev = FrequencyCounter()
print(dev.idn())
print(dev.measure_frequency(expected_frequency=50e6, resolution=0.1))
