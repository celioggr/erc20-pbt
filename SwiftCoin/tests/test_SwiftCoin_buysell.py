import pytest
from erc20_pbt import BuySellStateMachine


@pytest.fixture()
def contract2test(SwftCoin):
    yield SwftCoin


class SwftCoin(BuySellStateMachine):
    def __init__(self, accounts, contract2test):
        totalSupply = 1000
        contract = contract2test.deploy(
            1000, "SwiftCoin", 18, "SFC", {"from": accounts[0]}
        )
        BuySellStateMachine.__init__(self, accounts, contract, totalSupply)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(SwftCoin, accounts, contract2test)
