import brownie, pytest
from brownie import project


@pytest.fixture(scope="module")
def contract2test(accounts):
    token = project.load(
        "/home/honeybadger/novoteste/tests/stateful/BitAseanToken"
    ).BitAseanToken
    yield token


def test_transferFrom_not_allowed(contract2test, accounts):
    contract2test = contract2test.deploy(
        10000, "BitAseanToken", 10, "BAT", {"from": accounts[0]}
    )
    contract2test.approve(accounts[1], 100, {"from": accounts[0]})
    contract2test.transferFrom(
        accounts[0], accounts[2], 60, {"from": accounts[1]}
    )
    contract2test.approve(accounts[1], 0, {"from": accounts[0]})
    contract2test.transferFrom.call(
        accounts[0], accounts[2], 10, {"from": accounts[1]}
    )
