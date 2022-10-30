import numpy as np
import socket

class ENA():
    def __init__(self, address='e5062a.lan', port=5025):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.f = self.socket.makefile('rwb')
        assert self.idn()[1] == 'E5062A'

    def read(self):
        return self.f.readline()

    def write(self, s):
        self.f.write(bytes(s + "\n", 'ascii'))
        self.f.flush()

    def query(self, s):
        self.write(s)
        return self.read().decode('ascii').strip()

    def idn(self):
        return self.query("*IDN?").split(',')

    def set_frequency(self, frequency, port=1):
        self.write(f"SENS{port}:FREQ:CW {frequency:e}")

    def set_power(self, power, port=1):
        self.write(f"SOUR{port}:POW:CENT {power}")

    def set_active_trace(self, trace, channel=1):
        self.write(f"CALC{channel}:PAR{trace}:SEL")

    def get_trace_count(self, channel=1):
        count = self.query(f"CALC{channel}:PAR:COUNT?")
        return int(count)

    def get_trace_measurement(self, trace, channel=1):
        meas = self.query(f"CALC{channel}:PAR{trace}:DEF?")
        return meas

    def get_freq_data(self, channel=1):
        data = self.query(f"SENS{channel}:FREQ:DATA?")
        return np.array([float(x) for x in data.split(',')])

    def get_corrected_data(self, channel=1):
        data = self.query(f"CALC{channel}:DATA:SDAT?")
        data = np.array([float(x) for x in data.split(',')])
        c = np.empty(int(len(data)/2), dtype=np.complex64)
        c.real = data[0::2]
        c.imag = data[1::2]
        return c


if __name__ == "__main__":
    dev = ENA()
    print(dev.idn())
    dev.set_frequency(50e6)
    dev.set_power(0)
