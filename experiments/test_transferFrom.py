import brownie


def test_aprove(foo, accounts):
    assert foo.allowance(accounts[1], accounts[2]) == 0

    tx = foo.approve(accounts[2], 300, {"from": accounts[1]})
    assert "Approval" in tx.events
    expected = {"owner": accounts[1], "spender": accounts[2], "value": 300}
    assert tx.events["Approval"] == expected

    assert foo.allowance(accounts[1], accounts[2]) == 300

    tx = foo.approve(accounts[2], 50, {"from": accounts[1]})
    assert "Approval" in tx.events
    expected = {"owner": accounts[1], "spender": accounts[2], "value": 50}
    assert tx.events["Approval"] == expected

    assert foo.allowance(accounts[1], accounts[2]) == 50


def test_transferFrom(foo, accounts):
    """ allowance for this two accounts should be zero """
    assert foo.allowance(accounts[1], accounts[2]) == 0

    """ allow accounts[2] to spend 500 on on_behalf_of accounts[1] """
    foo.approve(accounts[2], 500, {"from": accounts[1]})
    assert foo.allowance(accounts[1], accounts[2]) == 500
    assert foo.balanceOf(accounts[1]) == 1000

    """ transferFrom(on_behalf_of,to,amount) """
    foo.transferFrom(accounts[1], accounts[4], 200, {"from": accounts[2]})
    assert foo.allowance(accounts[1], accounts[2]) == 300
    assert foo.balanceOf(accounts[1]) == 800
    assert foo.balanceOf(accounts[4]) == 200


def test_insufficient_allowance(foo, accounts):
    """ allowance for this two accounts should be zero """
    assert foo.allowance(accounts[1], accounts[2]) == 0
    """ allow accounts[2] to spend 500 on on_behalf_of accounts[1] """
    foo.approve(accounts[2], 500, {"from": accounts[1]})
    assert foo.allowance(accounts[1], accounts[2]) == 500
    """ will try to transfer more than allowed """
    with brownie.reverts("ERC20: transfer amount exceeds allowance"):
        foo.transferFrom(accounts[1], accounts[4], 1000, {"from": accounts[2]})

    assert foo.allowance(accounts[2], accounts[3]) == 0
    with brownie.reverts("ERC20: transfer amount exceeds allowance"):
        foo.transferFrom(accounts[3], accounts[4], 1, {"from": accounts[2]})


def test_transferFrom_same_address(foo, accounts):
    """ allowance for this two accounts should be zero """
    assert foo.allowance(accounts[1], accounts[2]) == 0

    """ allow accounts[2] to spend 500 on on_behalf_of accounts[1] """
    foo.approve(accounts[2], 500, {"from": accounts[1]})
    assert foo.allowance(accounts[1], accounts[2]) == 500
    assert foo.balanceOf(accounts[1]) == 1000

    """ transferFrom(on_behalf_of,to,amount) """
    foo.transferFrom(accounts[1], accounts[1], 200, {"from": accounts[2]})
    """ despite of transfering tokens from the same address as the destination
    allowance is decrease even though the balance stays the same"""
    assert foo.allowance(accounts[1], accounts[2]) == 300
    assert foo.balanceOf(accounts[1]) == 1000
    assert foo.balanceOf(accounts[2]) == 1000


def test_transferFrom_zero(foo, accounts):
    """ allowance for this two accounts should be zero """
    assert foo.allowance(accounts[1], accounts[2]) == 0

    """ allow accounts[2] to spend 500 on on_behalf_of accounts[1] """
    foo.approve(accounts[2], 500, {"from": accounts[1]})
    assert foo.allowance(accounts[1], accounts[2]) == 500
    assert foo.balanceOf(accounts[1]) == 1000

    """ transferFrom(on_behalf_of,to,amount) """
    foo.transferFrom(accounts[1], accounts[1], 0, {"from": accounts[2]})

    assert foo.allowance(accounts[1], accounts[2]) == 500
    assert foo.balanceOf(accounts[1]) == 1000
    assert foo.balanceOf(accounts[2]) == 1000
