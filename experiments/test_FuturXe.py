import brownie, pytest
from brownie import project


@pytest.fixture(scope="module")
def contract2test(accounts):
    token = project.load(
        "/home/honeybadger/novoteste/tests/stateful/FuturXe"
    ).FuturXe
    yield token


# this should not fail
def test_approve_100_withdraw_20_once(contract2test, accounts):
    contract2test = contract2test.deploy(
        10000, "FuturXe", "FXE", 10, {"from": accounts[0]}
    )
    contract2test.approve(accounts[1], 100, {"from": accounts[0]})
    print(
        "TransferFrom - {}".format(
            contract2test.transferFrom.call(
                accounts[0], accounts[2], 20, {"from": accounts[1]}
            )
        )
    )
    print(
        "Allowance - amount: {} ".format(
            contract2test.allowance.call(accounts[0], accounts[1])
        )
    )
    tx = contract2test.transferFrom(
        accounts[0], accounts[2], 20, {"from": accounts[1]}
    )
    print(tx.info())
    assert contract2test.balanceOf(accounts[2]) == 20


def test_transferFrom(contract2test, accounts):
    contract2test = contract2test.deploy(
        10000, "FuturXe", "FXE", 10, {"from": accounts[0]}
    )
    print(
        "Allowance of account[0] and account[2] is {}".format(
            contract2test.allowance(accounts[0], accounts[2])
        )
    )
    tx = contract2test.transferFrom(
        accounts[0], accounts[1], 21, {"from": accounts[2]}
    )
    print(tx)
    assert contract2test.balanceOf(accounts[0]) == 10000
