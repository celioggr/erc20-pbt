from brownie.test import strategy
import brownie.network.account
import brownie


class Edgecases:
    st_minter = strategy("address")

    def __init__(self):
        pass

    def rule_totalSupply_overflows(self, st_minter, st_receiver):
        uint256max = 2 ** 256 - 1
        if self.contract.owner == st_minter:
            tx = self.contract.mintToken(
                st_receiver, uint256max, {"from": st_minter}
            )
            self.totalSupply += uint256max
            self.balances[st_receiver] += uint256max
        else:
            with brownie.reverts():
                self.contract.mintToken(
                    st_receiver, uint256max, {"from": st_minter}
                )

    """
    def rule_totalSupply_underflows(self,st_minter,st_receiver):
            #To implement
            burn
    """
