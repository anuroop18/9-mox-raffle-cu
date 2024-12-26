import boa
import pytest
from eth_utils import to_wei
from moccasin.config import get_active_network

from script.deploy import deploy_raffle


@pytest.fixture(scope="session")
def owner():
    owner = get_active_network().get_default_account()
    return owner.address

@pytest.fixture(scope="function")
def user():
    user = boa.env.generate_address("user")
    boa.env.set_balance(user, to_wei(100, "ether"))
    return user

@pytest.fixture(scope="function")
def raffle(owner):
    with boa.env.prank(owner):
        return deploy_raffle()


# @pytest.fixture(scope="function")
# def raffle_funded(raffle, account):
#     boa.env.set_balance(account.address, SEND_VALUE*10)
#     with boa.env.prank(account.address):
#         raffle.fund(value=SEND_VALUE)
#     return raffle