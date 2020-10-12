import pytest
from erc20_pbt import StateMachine


@pytest.fixture()
def contract2test(HBToken):
    yield HBToken


class HBToken(StateMachine):
    def __init__(self, accounts, contract2test):
        contract = contract2test.deploy({"from": accounts[0]})
        StateMachine.__init__(self, accounts, contract, 5 * 10 ** 26)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(HBToken, accounts, contract2test)
