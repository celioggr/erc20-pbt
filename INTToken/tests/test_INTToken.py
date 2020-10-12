import pytest
from erc20_pbt import StateMachine


@pytest.fixture()
def contract2test(INT):
    yield INT


class INT(StateMachine):
    def __init__(self, accounts, contract2test):
        totalSupply = 1000000000000000
        contract = contract2test.deploy({"from": accounts[0]})
        StateMachine.__init__(self, accounts, contract, totalSupply)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(INT, accounts, contract2test)
