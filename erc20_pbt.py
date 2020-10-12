import os
import brownie
from brownie.test import strategy
from brownie.exceptions import VirtualMachineError


class StateMachine:
    st_amount = strategy("uint256")
    st_owner = strategy("address")
    st_spender = strategy("address")
    st_sender = strategy("address")
    st_receiver = strategy("address")

    def __init__(self, accounts, contract, totalSupply, DEBUG=None):
        self.accounts = accounts
        self.contract = contract
        self.totalSupply = totalSupply
        self.DEBUG = DEBUG != None or os.getenv("PBT_DEBUG", "no") == "yes"
        self.VERIFY_EVENTS = os.getenv("PBT_VERIFY_EVENTS") == "yes"
        self.VERIFY_RETURN_VALUES = (
            os.getenv("PBT_VERIFY_RETURN_VALUES") == "yes"
        )

    def setup(self):
        if self.DEBUG:
            print("setup()")
        self.allowances = dict()
        self.balances = {i: 0 for i in self.accounts}
        self.balances[self.accounts[0]] = self.totalSupply
        self.value_failure = False

    def teardown(self):
        if self.DEBUG:
            print("teardown()")
        if not self.value_failure:
            self.verifyTotalSupply()
            self.verifyAllBalances()
            self.verifyAllAllowances()

    def rule_transfer(self, st_sender, st_receiver, st_amount):
        if self.DEBUG:
            print(
                "transfer({}, {}, {})".format(st_sender, st_receiver, st_amount)
            )
        if st_amount <= self.balances[st_sender]:
            with normal():
                tx = self.contract.transfer(
                    st_receiver, st_amount, {"from": st_sender}
                )
                self.verifyTransfer(st_sender, st_receiver, st_amount)
                self.verifyEvent(
                    tx,
                    "Transfer",
                    {"from": st_sender, "to": st_receiver, "value": st_amount},
                )
                self.verifyReturnValue(tx, True)
        else:
            with brownie.reverts():
                self.contract.transfer(
                    st_receiver, st_amount, {"from": st_sender}
                )

    def rule_transferFrom(self, st_spender, st_owner, st_receiver, st_amount):
        if self.DEBUG:
            print(
                "transferFrom({}, {}, {}, [from: {}])".format(
                    st_owner, st_receiver, st_amount, st_spender
                )
            )
        if st_amount == 0 or (
            (st_owner, st_spender) in self.allowances.keys()
            and self.balances[st_owner] >= st_amount
            and self.allowances[(st_owner, st_spender)] >= st_amount
        ):
            with normal():
                tx = self.contract.transferFrom(
                    st_owner, st_receiver, st_amount, {"from": st_spender}
                )
                self.verifyTransfer(st_owner, st_receiver, st_amount)
                if st_amount != 0:
                    self.verifyAllowance(st_owner, st_spender, -st_amount)
                self.verifyEvent(
                    tx,
                    "Transfer",
                    {"from": st_owner, "to": st_receiver, "value": st_amount},
                )
                self.verifyReturnValue(tx, True)
        else:
            with brownie.reverts():
                self.contract.transferFrom(
                    st_owner, st_receiver, st_amount, {"from": st_spender}
                )

    def rule_approve(self, st_owner, st_spender, st_amount):
        if self.DEBUG:
            print("approve({}, {}, {})".format(st_owner, st_spender, st_amount))
        with (normal()):
            tx = self.contract.approve(
                st_spender, st_amount, {"from": st_owner}
            )
            self.verifyAllowance(st_owner, st_spender, st_amount)
            self.verifyEvent(
                tx,
                "Approval",
                {"owner": st_owner, "spender": st_spender, "value": st_amount},
            )
            self.verifyReturnValue(tx, True)

    def rule_transferAll(self, st_sender, st_receiver):
        self.rule_transfer(st_sender, st_receiver, self.balances[st_sender])

    def rule_approveAndTransferAll(self, st_owner, st_spender, st_receiver):
        amount = self.balances[st_owner]
        self.rule_approve(st_owner, st_spender, amount)
        self.rule_transferFrom(st_spender, st_owner, st_receiver, amount)

    def verifyTotalSupply(self):
        self.verifyValue(
            "totalSupply()", self.totalSupply, self.contract.totalSupply()
        )

    def verifyAllBalances(self):
        for account in self.balances:
            self.verifyBalance(account)

    def verifyAllAllowances(self):
        for (owner, spender) in self.allowances:
            self.verifyAllowance(owner, spender)

    def verifyBalance(self, addr):
        self.verifyValue(
            "balanceOf({})".format(addr),
            self.balances[addr],
            self.contract.balanceOf(addr),
        )

    def verifyTransfer(self, src, dst, amount):
        self.balances[src] -= amount
        self.balances[dst] += amount
        self.verifyBalance(src)
        self.verifyBalance(dst)

    def verifyAllowance(self, owner, spender, delta=None):
        if delta != None:
            if delta >= 0:
                self.allowances[(owner, spender)] = delta
            elif delta < 0:
                self.allowances[(owner, spender)] += delta
        self.verifyValue(
            "allowance({},{})".format(owner, spender),
            self.allowances[(owner, spender)],
            self.contract.allowance(owner, spender),
        )

    def verifyReturnValue(self, tx, expected):
        if self.VERIFY_RETURN_VALUES:
            self.verifyValue("return value", expected, tx.return_value)

    def verifyValue(self, msg, expected, actual):
        if expected != actual:
            self.value_failure = True
            raise AssertionError(
                "{} : expected value {}, actual value was {}".format(
                    msg, expected, actual
                )
            )

    def verifyEvent(self, tx, eventName, data):
        if self.VERIFY_EVENTS:
            if not eventName in tx.events:
                raise AssertionError(
                    "{}: event was not fired".format(eventName)
                )
            ev = tx.events[eventName]
            for k in data:
                if not k in ev:
                    raise AssertionError(
                        "{}.{}: absent event data".format(eventName, k)
                    )
                self.verifyValue("{}.{}".format(eventName, k), data[k], ev[k])


class MintingStateMachine(StateMachine):
    def __init__(self, accounts, contract, totalSupply, DEBUG=None):
        StateMachine.__init__(self, accounts, contract, totalSupply, DEBUG)

    def rule_mint(self, st_receiver, st_amount):
        if self.DEBUG:
            print("mint({}, {})".format(st_receiver, st_amount))
        if st_amount + self.totalSupply <= 2 ** 256 - 1:
            with normal():
                self.contract.mintToken(
                    st_receiver, st_amount, {"from": self.accounts[0]}
                )
                self.totalSupply += st_amount
                self.balances[st_receiver] += st_amount
                self.verifyBalance(st_receiver)
                self.verifyTotalSupply()
        else:
            with (brownie.reverts()):
                self.contract.mintToken(
                    st_receiver, st_amount, {"from": self.accounts[0]}
                )


class BurningStateMachine(StateMachine):
    def __init__(self, accounts, contract, totalSupply, DEBUG=None):
        StateMachine.__init__(self, accounts, contract, totalSupply, DEBUG)

    def rule_burn(self, st_sender, st_amount):
        if self.DEBUG:
            print("burn({}, {})".format(st_sender, st_amount))
        if st_amount >= 0 and self.balances[st_sender] >= st_amount:
            with normal():
                tx = self.contract.burn(st_amount, {"from": st_sender})
                self.totalSupply -= st_amount
                self.balances[st_sender] -= st_amount
                self.verifyBalance(st_sender)
                self.verifyTotalSupply()
                self.verifyEvent(
                    tx, "Burn", {"from": st_sender, "value": st_amount}
                )
        else:
            with (brownie.reverts()):
                self.contract.burn(st_amount, {"from": st_sender})

    def rule_burn_all(self, st_sender):
        self.rule_burn(st_sender, self.balances[st_sender])


class BuySellStateMachine(StateMachine):
    INITIAL_BUY_PRICE = 1
    INITIAL_SELL_PRICE = 1

    def __init__(self, accounts, contract, totalSupply, DEBUG=None):
        StateMachine.__init__(self, accounts, contract, totalSupply, DEBUG)

    def setup(self):
        # Base state machine setup
        StateMachine.setup(self)

        # Set initial prices
        self.buyPrice = self.INITIAL_BUY_PRICE
        self.sellPrice = self.INITIAL_SELL_PRICE

        # Set sell and buy price
        self.contract.setPrices(
            self.sellPrice, self.buyPrice, {"from": self.accounts[0]}
        )

        # Set up model for ether balance
        self.ethBalances = {i: i.balance() for i in self.accounts}
        self.ethBalances[self.contract] = self.contract.balance()

        # Model contract balance as well
        self.balances[self.contract] = 0

    def teardown(self):
        StateMachine.teardown(self)
        for x in self.ethBalances:
            self.verifyEthBalance(x)

    def rule_setPrices(self, st_amount):
        if self.DEBUG:
            print("setPrices({}, {})".format(st_amount, st_amount))
        self.buyPrice = st_amount
        self.sellPrice = st_amount
        self.contract.setPrices(
            self.sellPrice, self.buyPrice, {"from": self.accounts[0]}
        )
        self.verifyValue("buyPrice", self.buyPrice, self.contract.buyPrice())
        self.verifyValue("sellPrice", self.sellPrice, self.contract.sellPrice())

    def rule_sell(self, st_sender, st_amount):
        if self.DEBUG:
            print("sell({}, {})".format(st_sender, st_amount))
        ether = st_amount * self.sellPrice
        if (
            self.balances[st_sender] >= st_amount
            and self.ethBalances[self.contract] >= ether
        ):
            with normal():
                tx = self.contract.sell(st_amount, {"from": st_sender})
                self.verifySale(st_sender, self.contract, st_amount, ether, tx)
        else:
            with (brownie.reverts()):
                self.contract.sell(st_amount, {"from": st_sender})

    def rule_buy(self, st_sender, st_amount):
        if self.DEBUG:
            print("buy({}, {})".format(st_sender, st_amount))
        if (
            self.buyPrice > 0
            and self.ethBalances[st_sender] >= st_amount
            and self.balances[self.contract] >= st_amount // self.buyPrice
        ):
            with normal():
                tx = self.contract.buy({"from": st_sender, "value": st_amount})
                self.verifySale(
                    self.contract,
                    st_sender,
                    st_amount // self.buyPrice,
                    st_amount,
                    tx,
                )
        elif self.ethBalances[st_sender] >= st_amount:
            with (brownie.reverts()):
                self.contract.buy({"from": st_sender, "value": st_amount})

    def rule_sellAll(self, st_sender):
        self.rule_sell(st_sender, self.balances[st_sender])

    def verifyEthBalance(self, addr):
        self.verifyValue(
            "ethBalance({})".format(addr),
            self.ethBalances[addr],
            addr.balance(),
        )

    def verifySale(self, a, b, tokens, ether, tx):
        self.balances[a] -= tokens
        self.balances[b] += tokens
        self.ethBalances[a] += ether
        self.ethBalances[b] -= ether
        self.verifyBalance(a)
        self.verifyBalance(b)
        self.verifyEthBalance(a)
        self.verifyEthBalance(b)
        self.verifyEvent(tx, "Transfer", {"from": a, "to": b, "value": tokens})


def patch_hypothesis_for_seed_handling(seed):
    import hypothesis

    h_run_state_machine = hypothesis.stateful.run_state_machine_as_test

    def run_state_machine(state_machine_factory, settings=None):
        state_machine_factory._hypothesis_internal_use_seed = seed
        h_run_state_machine(state_machine_factory, settings)

    hypothesis.stateful.run_state_machine_as_test = run_state_machine


def patch_brownie_for_assertion_detection():
    from brownie.test.managers.runner import RevertContextManager
    from brownie.exceptions import VirtualMachineError

    f = RevertContextManager.__exit__

    def alt_exit(self, exc_type, exc_value, traceback):
        if exc_type is VirtualMachineError:
            exc_value.__traceback__.tb_next = None
            if exc_value.revert_type != "revert":
                return False
        return f(self, exc_type, exc_value, traceback)

    RevertContextManager.__exit__ = alt_exit


def register_hypothesis_profiles():
    import hypothesis
    from hypothesis import settings, Verbosity, Phase

    stateful_step_count = int(os.getenv("PBT_STATEFUL_STEP_COUNT", 10))
    max_examples = int(os.getenv("PBT_MAX_EXAMPLES", 100))
    derandomize = True
    seed = int(os.getenv("PBT_SEED", 0))

    if seed != 0:
        patch_hypothesis_for_seed_handling(seed)
        derandomize = False

    patch_brownie_for_assertion_detection()

    settings.register_profile(
        "generate",
        stateful_step_count=stateful_step_count,
        max_examples=max_examples,
        phases=[Phase.generate],
        report_multiple_bugs=True,
        derandomize=derandomize,
        print_blob=True,
    )

    settings.register_profile(
        "shrinking",
        stateful_step_count=stateful_step_count,
        max_examples=max_examples,
        phases=[Phase.generate, Phase.shrink],
        report_multiple_bugs=True,
        derandomize=derandomize,
        print_blob=True,
    )


class NoRevertContextManager:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            return True
        import traceback

        if exc_type is VirtualMachineError:
            exc_value.__traceback__.tb_next = None
        elif exc_type is AssertionError:
            exc_value.__traceback__.tb_next = None
        return False


def normal():
    return NoRevertContextManager()
