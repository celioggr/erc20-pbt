from brownie import accounts


def test_aprove_event(foo, accounts):
    tx = foo.approve(accounts[2], 300, {"from": accounts[1]})
    assert "Approval" in tx.events
    expected = {"owner": accounts[1], "spender": accounts[2], "value": 300}
    assert tx.events["Approval"] == expected


def test_transfer_event(foo, accounts):
    tx = foo.transfer(accounts[2], 300, {"from": accounts[1]})
    assert "Transfer" in tx.events
    expected = {"from": accounts[1], "to": accounts[2], "value": 300}
    assert tx.events["Transfer"] == expected


def test_transferFrom_event(foo, accounts):
    """ allow accounts[2] to spend 500 on on_behalf_of accounts[1] """
    foo.approve(accounts[2], 500, {"from": accounts[1]})
    tx = foo.transferFrom(accounts[1], accounts[4], 300, {"from": accounts[2]})
    assert "Approval" in tx.events
    assert "Transfer" in tx.events

    """ tx.events["Approval"] contains allowance value updated after transferFrom is executed """
    expected_approval = {
        "owner": accounts[1],
        "spender": accounts[2],
        "value": 200,
    }
    expected_transfer = {"from": accounts[1], "to": accounts[4], "value": 300}
    assert tx.events["Approval"] == expected_approval
    assert tx.events["Transfer"] == expected_transfer
