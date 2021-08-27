"""QuantumComputer Module

Defines a quantum circuit with an input register and a memory register onto which
instructions can be encoded as a bitstring. The core quantum computer circuit executes
the instructions. The state of the memory register is read out and returned to the
user.

"""

import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute


class QuantumComputer:
    """
    QuantumComputer Class
    """

    def __init__(self, data_size: int, addr_size: int):
        self.data_size = data_size
        self.addr_size = addr_size

        self.optype = QuantumRegister(1, name="optype")
        self.opdata = QuantumRegister(self.data_size, name="opdata")
        self.opaddr = QuantumRegister(self.addr_size, name="opaddr")
        self.address = QuantumRegister(self.addr_size, name="address")
        self.data = QuantumRegister(self.data_size, name="data")

        self.meas = ClassicalRegister(self.addr_size + self.data_size, name="meas")

        self.circuit = QuantumCircuit(
            self.address, self.data, self.opaddr, self.opdata, self.optype, self.meas
        )

    def program(self, program):
        """
        Encode a program (set of instructions) onto the quantum computer.
        """
        self.circuit.initialize(program + "0" * (self.data.size + self.address.size))
        self.circuit.barrier()

    def _init_memory(self):
        """
        Initialize the memory register in uniform superposition for assignment.
        """
        self.circuit.h(self.address)
        self.circuit.barrier()

    def _add_store_op(self):
        """
        Add instruction handling to the quantum computer circuit for the store operation.
        """
        self.circuit.h(self.address)
        self.circuit.barrier()

        self.circuit.x(self.opaddr)

        for bit in range(0, self.address.size, 1):
            self.circuit.mct(
                self.optype[:] + self.opaddr[bit : bit + 1],
                self.address[self.address.size - 1 - bit],
            )

        for bit in range(0, self.data.size, 1):
            self.circuit.mct(
                self.optype[:] + self.opdata[bit : bit + 1] + self.address[:],
                self.data[self.data.size - 1 - bit],
            )

        for bit in range(self.address.size - 1, -1, -1):
            self.circuit.mct(
                self.optype[:] + self.opaddr[bit : bit + 1],
                self.address[self.address.size - 1 - bit],
            )

        self.circuit.x(self.optype)

        self.circuit.barrier()

    def run(self):
        """
        Add all supported instruction handlers to the quantum computer circuit.
        """
        self._add_store_op()

    def get_state(self):
        """
        Measure the state of the memory register and return the result.
        """
        self.circuit.measure(self.address[:], self.meas[: self.addr_size])
        self.circuit.measure(
            self.data[:], self.meas[self.addr_size : self.addr_size + self.data_size]
        )

        self.circuit = self.circuit.reverse_bits()

        state = np.zeros(2 ** self.address.size)
        for reg in (
            execute(self.circuit.decompose(), Aer.get_backend("aer_simulator"))
            .result()
            .get_counts()
            .keys()
        ):
            state[int(reg[: self.address.size], 2)] = int(reg[self.address.size :], 2)
        return state
