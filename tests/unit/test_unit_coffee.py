from eth_utils import to_wei
import boa

from tests.conftest import coffee, SEND_VALUE

RANDOM_USER = boa.env.generate_address("random_user")


def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts():
        coffee.fund()

def test_fund_with_money(coffee, account):
    boa.env.set_balance(account.address, SEND_VALUE)
    coffee.fund(value=SEND_VALUE)
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded, account):
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Only owner can withdraw"):
            coffee_funded.withdraw()

def test_owner_can_withdraw_single_funder(coffee_funded, account):
    boa.env.set_balance(coffee_funded.OWNER(), SEND_VALUE)
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.fund(value=SEND_VALUE)
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0
 

def test_owner_can_withdraw_multiple_funders(coffee_funded):
    number_of_funders = 10
    for i in range(number_of_funders):
        user = boa.env.generate_address(i)
        boa.env.set_balance(user, SEND_VALUE * 2)
    starting_fund_me_balance = boa.env.get_balance(coffee_funded.address)
    starting_owner_balance = boa.env.get_balance(coffee_funded.OWNER())

    # Withdraw
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()

    assert boa.env.get_balance(coffee_funded.address) == 0
    assert boa.env.get_balance(coffee_funded.OWNER()) == starting_owner_balance + starting_fund_me_balance
