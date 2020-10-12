import pytest
from erc20_pbt import StateMachine


@pytest.fixture()
def contract2test(LinkToken):
    yield LinkToken


class LinkToken(StateMachine):
    def __init__(self, accounts, contract2test):
        contract = contract2test.deploy({"from": accounts[0]})
        StateMachine.__init__(self, accounts, contract, 10 ** 27)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(LinkToken, accounts, contract2test)
