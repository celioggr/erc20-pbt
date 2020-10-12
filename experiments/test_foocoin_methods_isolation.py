@pytest.fixture(scope="module", autouse=True)
def shared_setup(module_isolation, web3):
    assert web3.eth.blockNumber == 1
    pass


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="module")
def foo(FooCoin, accounts):
    t = FooCoin.deploy(10000, "FooCoin", "FCN", 18, {"from": accounts[0]})
    yield t
    # test_final_blockchain_state(foo,web3)


def test_details(foo):
    assert foo.name() == "FooCoin"
    assert foo.symbol() == "FCN"
    assert foo.decimals() == 18
    assert foo.totalSupply() == 10000


def test_transfer(foo, accounts):
    foo.transfer(accounts[1], 100, {"from": accounts[0]})
    assert foo.balanceOf(accounts[0]) == 9900


def test_chain_reverted(foo, accounts):
    assert foo.balanceOf(accounts[0]) == 10000


def test_approval(foo, accounts):
    foo.approve(accounts[1], 500, {"from": accounts[0]})
    assert foo.allowance(accounts[0], accounts[1]) == 500
    assert foo.balanceOf(accounts[0]) == 10000


def test_transfer_funds_on_behalf_of(foo, accounts):
    foo.approve(accounts[1], 500, {"from": accounts[0]})
    assert foo.allowance(accounts[0], accounts[1]) == 500
    assert foo.balanceOf(accounts[0]) == 10000
    """ transferFrom(on_behalf_of,to,amount) """
    foo.transferFrom(accounts[0], accounts[2], 200, {"from": accounts[1]})
    assert foo.allowance(accounts[0], accounts[1]) == 300
    assert foo.balanceOf(accounts[0]) == 9800
    assert foo.balanceOf(accounts[2]) == 200


def test_reverted_accounts(foo, accounts):
    assert foo.balanceOf(accounts[0]) == 10000
    assert foo.balanceOf(accounts[2]) == 0
