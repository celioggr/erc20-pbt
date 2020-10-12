import pytest
from erc20_pbt import StateMachine


@pytest.fixture()
def contract2test(EIP20):
    yield EIP20


class Consensys(StateMachine):
    def __init__(self, accounts, contract2test):
        totalSupply = 1000
        contract = contract2test.deploy(
            1000, "Consensys", 10, "XYZ", {"from": accounts[0]}
        )
        StateMachine.__init__(self, accounts, contract, totalSupply)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(Consensys, accounts, contract2test)
