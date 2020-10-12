import pytest
from brownie import project

"""
# test isolation, always use
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# contract deployment
@pytest.fixture(scope="module")
def foo(accounts):
    #BuggyA = project.load('/home/honeybadger/BuggyContractA')
    #token = BuggyA.deploy(10000,"FooCoin", "FCN", 18, {'from': accounts[0]})
    BuggyA = project.load('/home/honeybadger/GoodContract').GoodContract
    token = BuggyA.deploy(10000,"FooCoin", "FCN", 18, {'from': accounts[0]})
    token.transfer(accounts[1], 1000, {"from": accounts[0]})
    token.transfer(accounts[2], 1000, {"from": accounts[0]})
    token.transfer(accounts[3], 1000, {"from": accounts[0]})
    yield token
"""
