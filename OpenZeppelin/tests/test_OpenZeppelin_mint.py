import pytest
from erc20_pbt import MintingStateMachine


@pytest.fixture()
def contract2test(OpenZeppelin):
    yield OpenZeppelin


class OpenZeppelin(MintingStateMachine):
    def __init__(self, accounts, contract2test):
        totalSupply = 1000
        contract = contract2test.deploy(
            1000, "OpenZeppelin", "OPZ", 10, {"from": accounts[0]}
        )
        contract.mintToken = contract.mint
        MintingStateMachine.__init__(self, accounts, contract, totalSupply)


def test_stateful(contract2test, accounts, state_machine):
    state_machine(OpenZeppelin, accounts, contract2test)
