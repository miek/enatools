import socket

class ENA():
    def __init__(self, address='10.64.10.135', port=5025):
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

    def set_frequency(self, frequency):
        self.write(f"SENS1:FREQ:CW {frequency:e}")

if __name__ == "__main__":
    dev = ENA()
    print(dev.idn())
    dev.set_frequency(50e6)
