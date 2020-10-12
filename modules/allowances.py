class Allowances:
    def __init__(self):
        pass

    def rule_increase_the_allowance(self, st_owner, st_spender, st_amount):
        tx = self.contract.increaseAllowance(
            st_spender, st_amount, {"from": st_owner}
        )
        assert "Approval" in tx.events

        current_allowance = 0
        if (st_owner, st_spender) in self.allowances.keys():
            current_allowance = self.allowances[(st_owner, st_spender)]
        """ Update local allowances """
        self.allowances[(st_owner, st_spender)] = current_allowance + st_amount

    """
        Requirements:
            -spender must have allowance for the caller of at least
    """

    def rule_decrease_the_allowance(self, st_spender, st_owner, st_amount):
        if (st_owner, st_spender) in self.allowances.keys():
            if self.allowances[(st_owner, st_spender)] >= st_amount:
                tx = self.contract.decreaseAllowance(
                    st_spender, st_amount, {"from": st_owner}
                )
                assert "Approval" in tx.events
                """ Update local allowances """
                self.allowances[(st_owner, st_spender)] -= st_amount
            else:
                with brownie.reverts():
                    self.contract.decreaseAllowance(
                        st_spender, st_amount, {"from": st_owner}
                    )
