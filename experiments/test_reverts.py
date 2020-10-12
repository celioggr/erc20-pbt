import brownie, pytest, re

""" override foo fixture from conftest
@pytest.fixture(scope="module")
def foo(foo,accounts,FooCoin):
    token = FooCoin.deploy(2**64,"FooCoin", "FCN", 18, {'from': accounts[0]})
    yield token
"""


def test_uint256_overflow(foo, accounts):
    with pytest.raises(OverflowError) as exc_info:
        foo.transfer(accounts[2], 2 ** 256, {"from": accounts[0]})
    assert exc_info.type is OverflowError
    assert exc_info.match("is outside allowable range for uint256")


def test_try_underflow(foo, accounts):
    with pytest.raises(brownie.exceptions.VirtualMachineError) as exc_info:
        foo.transfer(accounts[2], 10000, {"from": accounts[1]})
    assert exc_info.type is brownie.exceptions.VirtualMachineError
    assert exc_info.match("ERC20: transfer amount exceeds balance")
