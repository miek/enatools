from gpib_ctypes import Gpib

class GPIBDevice(Gpib.Gpib):
    def query(self, s, response_length=1024):
        self.write(s)
        return self.read(response_length).decode('ascii').strip()

    def write(self, s):
        super().write(bytes(s, 'ascii'))

    def idn(self):
        return self.query('*IDN?').split(',')
