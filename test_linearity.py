import time
import sys
from ena import ENA
from power_meter import PowerMeter

frequencies = [
    300e3,
    50e6,
    1.5e9,
    3e9,
]

powers = [
    -5,
    -2.5,
    2.5,
    5,
    7.5,
    10,
]

port = 1
if len(sys.argv) > 1:
    port = int(sys.argv[1])

ena = ENA()
pm = PowerMeter()

def test(f, power, port):
    ena.set_frequency(f, port)
    ena.set_power(power)
    pm.set_frequency(f)
    time.sleep(0.3)
    return pm.measure_power(expected_power=power, resolution=0.001)

for f in frequencies:

    print(f"RF Output Level Linearity Test (@ Port {port})")
    print(f"CW Frequency: {f/1e6:.2f} MHz (relative to 0 dBm reference)")
    print("Power level\tTest result")
    print("-----------\t-----------")
    baseline = test(f, 0, port)
    for p in powers:
        result = test(f, p, port)
        result = result - p - baseline
        result_pass_fail = "PASS" if abs(result) < 0.75 else "FAIL"
        print(f"{p} dBm    \t{result:f}\t{result_pass_fail}")

    print("")
