import pulser
import numpy as np
from pprint import pprint
from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser.waveforms import RampWaveform, BlackmanWaveform

L = 4
square = np.array([[i, j] for i in range(L) for j in range(L)], dtype=float)
square -= np.mean(square, axis=0)
square *= 5

qubits = dict(enumerate(square))
reg = Register(qubits)

reg1 = Register(qubits)  # Copy of 'reg' to keep the original intact

seq = Sequence(reg, Chadoq2)
seq.declare_channel("ch1", "rydberg_local")

print("\nAvailable channels after declaring 'ch1':")
pprint(seq.declared_channels)

seq.target(1, "ch1")
simple_pulse = Pulse.ConstantPulse(200, 2, -10, 0)
seq.add(simple_pulse, "ch1")
seq.delay(100, "ch1")

duration = 1000
amp_wf = BlackmanWaveform(duration, np.pi / 2)  # Duration: 1000 ns, Area: pi/2
detuning_wf = RampWaveform(
    duration, -20, 20
)  # Duration: 1000ns, linear sweep from -20 to 20 rad/µs

#amp_wf.draw()

amp_wf.integral  # dimensionless
complex_pulse = Pulse(amp_wf, detuning_wf, phase=0)
complex_pulse.draw()