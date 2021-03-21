import time
import sys
from ena import ENA
from power_meter import PowerMeter

frequencies = [
    300e3,

    1.5e6,
    3e6,
    7e6,
    15e6,
    275e6,
    575e6,
    875e6,

    1.175e9,
    1.5e9,
    1.775e9,
    2e9,
    2.375e9,
    2.675e9,
    3e9,
]

port = 1
if len(sys.argv) > 1:
    port = int(sys.argv[1])

ena = ENA()
pm = PowerMeter()

def test_freq(f, port):
    ena.set_frequency(f, port)
    pm.set_frequency(f)
    time.sleep(0.1)
    return pm.measure_power(expected_power=0, resolution=0.001)

print(f"Level Accuracy Test (@ Port {port})")
print("Power level\tFrequency\tTest limit\tTest result")
print("-----------\t---------\t----------\t-----------")
baseline = test_freq(50e6, port)
result_pass_fail = "PASS" if abs(baseline) < 0.8 else "FAIL"
print(f"0         \t50M      \t+/- 0.8   \t{baseline:f}\t{result_pass_fail}")
print("")


print(f"Level Flatness Test (@ Port {port})")
print("Frequency\tResult")
print("---------\t------")

for f in frequencies:
    result = test_freq(f, port)
    result = result - baseline
    result_pass_fail = "PASS" if abs(result) < 1 else "FAIL"
    print(f"{f/1e6:.2f} MHz \t{result:f}\t{result_pass_fail}")
