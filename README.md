# qcpu

**qcpu** is a software development kit for designing, building, and testing parameterized quantum circuits that accept *quantum programs* (sets of *quantum instructions*) as input and return the result of executing said quantum instructions as output.

## Usage
This code constructs a quantum computer that represents memory data with 4 qubits (max representable integer is 15 in decimal) and memory addresses with 2 qubits (4 total addresses). The computer is then given the instruction `"1111111"`. 
1. The first bit (`1`) is the opcode for the store instruction.
2. The next four bits represent the data to store (`1111`, 15 in decimal).
3. The final two bits specify the address in which to store the data (`11`, the fourth and final memory address).

Thus,  `"1111111"` represents the instruction to store 15 in the fourth memory address. When we take a look at the state of the memory register after running our 1-instruction program on our computer, we see that 15 is stored in the fourth memory address as expected.

```python
>>> from qcpu import QuantumComputer
>>> computer = QuantumComputer(4, 2)
>>> computer.program("1111111")
>>> computer.run()
>>> state = computer.get_state()
>>> print(state)
[ 0.  0.  0. 15.]
```
