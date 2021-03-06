import pytest
from erc20_pbt import MintingStateMachine


@pytest.fixture()
def contract2test(BitAseanToken):
    yield BitAseanToken


class BitAseanToken(MintingStateMachine):
    def __init__(self, accounts, contract2test):
        totalSupply = 1000
        contract = contract2test.deploy(
            1000, "BitAseanToken", 10, "BAT", {"from": accounts[0]}
        )
        MintingStateMachine.__init__(self, accounts, contract, totalSupply)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(BitAseanToken, accounts, contract2test)
