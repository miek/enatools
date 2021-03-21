from gpib_device import GPIBDevice

class PowerMeter(GPIBDevice):
    def __init__(self, gpib_device=0, gpib_address=13):
        super().__init__(gpib_device, gpib_address)
        idn_response = self.idn()
        assert idn_response[1] == 'E4419B'

    def measure_power(self, *, expected_power=None, resolution=None):
        cmd = 'MEAS1?'
        if expected_power is not None:
            cmd += f' {expected_power:e}DBM'
            if resolution is not None:
                cmd += f', {resolution}'

        return float(self.query(cmd))

    def set_frequency(self, frequency):
        self.write(f"SENS1:FREQ {frequency:e}")

if __name__ == "__main__":
    dev = PowerMeter()
    print(dev.idn())
    dev.set_frequency(300e3)
    print(dev.measure_power(expected_power=0, resolution=0.01))
