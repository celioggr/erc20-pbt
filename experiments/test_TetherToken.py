import brownie, pytest
from brownie import project

"""
    Mitigation of race condition when using both approve and transferFrom
    https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
"""


@pytest.fixture()
def contract2test():
    token = project.load("/home/honeybadger/2test").TetherToken
    yield token


"""
    If there is a previous allowance already defined between two accounts, then
    subsequent calls to approve will not be allowed.
    Allowance between those two accounts needs to be set to 0 first and then can be
    changed
"""
"""
def test_approve(contract2test,accounts):
    contract2test=contract2test.deploy(1000,"TetherToken","TET",18,{"from": accounts[0]})
    contract2test.approve(accounts[2],904632722760382038031595418818832251216267922681632235559156899113536344216,{"from":accounts[0]})
    contract2test.approve(accounts[2],0,{"from":accounts[0]})
    contract2test.approve(accounts[2],1,{"from": accounts[0]})
"""


def test_assert(contract2test, accounts):
    contract2test = contract2test.deploy(
        1000, "TetherToken", "TET", 18, {"from": accounts[0]}
    )
    with brownie.reverts():
        tx = contract2test.transfer(accounts[1], 10, {"from": accounts[2]})
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(dir(tx))
        assert 1 == 0
