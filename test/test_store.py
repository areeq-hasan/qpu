import numpy as np
from qcpu import QuantumComputer


def test_store():
    """
    Test storing and retrieving values from the memory register.
    """
    computer = QuantumComputer(1, 15, 2)
    computer.program("0011111")
    computer.run()
    state = computer.get_state()
    assert not np.any(state[:3])
    assert state[3] == 7
