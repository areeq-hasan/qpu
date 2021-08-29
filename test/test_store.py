"""Test Store"""

import numpy as np
from qpu import QuantumComputer


def test_store():
    """
    Test storing and retrieving values from the memory register.
    """
    computer = QuantumComputer(4, 2)
    computer.program("1111111")
    computer.run()
    state = computer.get_state()
    assert not np.any(state[:3])
    assert state[3] == 15
