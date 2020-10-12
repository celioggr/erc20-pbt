import pytest
from erc20_pbt import MintingStateMachine


@pytest.fixture()
def contract2test(FuturXe):
    yield FuturXe


class FuturXe(MintingStateMachine):
    def __init__(self, accounts, contract2test):
        totalSupply = 1000
        contract = contract2test.deploy(
            1000, "FuturXe", "FXE", 10, {"from": accounts[0]}
        )
        MintingStateMachine.__init__(
            self, accounts, contract, totalSupply, True
        )


def test_stateful(contract2test, accounts, state_machine):
    state_machine(FuturXe, accounts, contract2test)
