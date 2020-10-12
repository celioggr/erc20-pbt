from brownie.test import strategy
import brownie


class TokenSupply:
    st_minter = strategy("address")

    def __init__(self):
        pass

    def rule_mint(self, st_receiver, st_minter, st_amount):
        print(st_amount)
        if self.contract.owner() == st_minter:
            self.contract.mintToken(st_receiver, st_amount, {"from": st_minter})
            self.totalSupply += st_amount
            self.balances[st_receiver] += st_amount
        else:
            with brownie.reverts():
                self.contract.mintToken(
                    st_receiver, st_amount, {"from": st_minter}
                )

    """
    def rule_totalSupply_underflows(self,st_minter,st_receiver):
            #To implement
            burn
    """
