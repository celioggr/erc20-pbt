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

    """Overwrite state machine brownie.reverts() to search for a revert comment string"""

    def rule_transfer(self, st_sender, st_receiver, st_amount):
        if self.DEBUG:
            print(
                "transfer({}, {}, {})".format(st_sender, st_receiver, st_amount)
            )
        if st_amount <= self.balances[st_sender]:
            tx = self.contract.transfer(
                st_receiver, st_amount, {"from": st_sender}
            )
            self.verifyTransfer(st_sender, st_receiver, st_amount)
            self.verifyEvent(
                tx,
                "Transfer",
                {"from": st_sender, "to": st_receiver, "value": st_amount},
            )
        else:
            with brownie.reverts("revert"):
                self.contract.transfer(
                    st_receiver, st_amount, {"from": st_sender}
                )

    """Overwrite state machine brownie.reverts() to search for a revert comment string"""

    def rule_transferFrom(self, st_spender, st_owner, st_receiver, st_amount):
        if self.DEBUG:
            print(
                "transferFrom({}, {}, {}, [from: {}])".format(
                    st_owner, st_receiver, st_amount, st_spender
                )
            )
        if st_amount == 0 or (
            (st_owner, st_spender) in self.allowances.keys()
            and self.balances[st_owner] >= st_amount
            and self.allowances[(st_owner, st_spender)] >= st_amount
        ):
            tx = self.contract.transferFrom(
                st_owner, st_receiver, st_amount, {"from": st_spender}
            )
            self.verifyTransfer(st_owner, st_receiver, st_amount)
            self.verifyAllowance(st_owner, st_spender, -st_amount)
            self.verifyEvent(
                tx,
                "Transfer",
                {"from": st_owner, "to": st_receiver, "value": st_amount},
            )
        else:
            with brownie.reverts("revert"):
                tx = self.contract.transferFrom(
                    st_owner, st_receiver, st_amount, {"from": st_spender}
                )


def test_stateful(contract2test, accounts, state_machine):
    state_machine(BNB, accounts, contract2test)
