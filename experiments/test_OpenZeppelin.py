import brownie, pytest
from brownie import project


@pytest.fixture(scope="module")
def contract2test(accounts):
    token = project.load(
        "/home/honeybadger/novoteste/tests/stateful/OpenZeppelin"
    ).OpenZeppelin
    yield token


def test_wrong_allowance(contract2test, accounts):
    contract2test = contract2test.deploy(
        1000, "OpenZeppelin", "OPZ", 18, {"from": accounts[0]}
    )
    contract2test.approve(accounts[0], 15, {"from": accounts[0]})
    tx = contract2test.transferFrom(
        accounts[0], accounts[0], 0, {"from": accounts[0]}
    )
    # print(contract2test. 66.67 |     62.5 |       50 |    69.23allowance(accounts[0],accounts[0]))
    # assert contract2test.allowance(accounts[0],accounts[0]) == 1
    # print(tx.events)


def test_revert(contract2test, accounts):
    contract2test = contract2test.deploy(
        1000, "OpenZeppelin", "OPZ", 18, {"from": accounts[0]}
    )
    contract2test.approve(accounts[0], 0, {"from": accounts[0]})
    tx = contract2test.transferFrom(
        accounts[0], accounts[0], 0, {"from": accounts[2]}
    )
    # print(tx.events)


def test_revert_transferFrom(contract2test, accounts):
    contract2test = contract2test.deploy(
        1000, "OpenZeppelin", "OPZ", 18, {"from": accounts[0]}
    )
    tx = contract2test.transferFrom(
        accounts[1], accounts[0], 0, {"from": accounts[2]}
    )
    # print(tx.events)


def test_transferFrom_without_having_prev_allowance(contract2test, accounts):
    contract2test = contract2test.deploy(
        1000, "OpenZeppelin", "OPZ", 18, {"from": accounts[0]}
    )
    tx = contract2test.transferFrom(
        accounts[0], accounts[0], 0, {"from": accounts[0]}
    )
    print(tx.events)
    print("{} - {} - {}".format(accounts[0], accounts[1], accounts[2]))
