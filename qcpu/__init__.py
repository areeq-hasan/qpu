import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute


class QuantumComputer:
    def __init__(self, n_op: int, n_int: int, n_addr: int):
        self.n_op = n_op
        self.n_int = n_int
        self.n_addr = n_addr

        self.addr_reg_size = max(self.n_addr.bit_length(), 1)
        self.data_reg_size = max(self.n_int.bit_length(), 1)

        self.optype = QuantumRegister(max(self.n_op.bit_length(), 1), name="optype")
        self.opdata = QuantumRegister(max(self.n_int.bit_length(), 1), name="opdata")
        self.opaddr = QuantumRegister(self.addr_reg_size, name="opaddr")
        self.address = QuantumRegister(self.addr_reg_size, name="address")
        self.data = QuantumRegister(self.data_reg_size, name="data")

        self.meas = ClassicalRegister(
            self.addr_reg_size + self.data_reg_size, name="meas"
        )

        self.circuit = QuantumCircuit(
            self.address, self.data, self.opaddr, self.opdata, self.optype, self.meas
        )

    def program(self, program):
        self.circuit.initialize(program + "0" * (self.data.size + self.address.size))
        self.circuit.barrier()

    def _init_memory(self):
        self.circuit.h(self.address)
        self.circuit.barrier()

    def _add_store_op(self):
        self.circuit.h(self.address)
        self.circuit.barrier()

        self.circuit.x(self.optype)
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

        self.circuit.x(self.opaddr)
        self.circuit.x(self.optype)

        self.circuit.barrier()

    def run(self):
        self._add_store_op()

    def get_state(self):
        self.circuit.measure(self.address[:], self.meas[: self.addr_reg_size])
        self.circuit.measure(
            self.data[:],
            self.meas[self.addr_reg_size : self.addr_reg_size + self.data_reg_size],
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
