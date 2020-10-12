import pytest
from erc20_pbt import StateMachine


@pytest.fixture()
def contract2test(BNB):
    yield BNB


class BNB(StateMachine):
    def __init__(self, accounts, contract2test):
        contract = contract2test.deploy(
            1000, "BNB", 18, "BNB", {"from": accounts[0]}
        )
        StateMachine.__init__(self, accounts, contract, 1000)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(BNB, accounts, contract2test)
