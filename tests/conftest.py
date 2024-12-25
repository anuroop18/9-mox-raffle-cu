import boa
import pytest
from eth_utils import to_wei
from moccasin.config import get_active_network

from script.deploy import deploy_raffle
from script.deploy_mocks import deploy_feed

SEND_VALUE = to_wei(1, "ether")

@pytest.fixture(scope="session")
def account():
    return get_active_network().get_default_account()

@pytest.fixture(scope="session")
def eth_usd_pricefeed():
    return deploy_feed()

@pytest.fixture(scope="function")
def raffle(eth_usd_pricefeed):
    return deploy_raffle(eth_usd_pricefeed)

@pytest.fixture(scope="function")
def raffle_funded(raffle, account):
    boa.env.set_balance(account.address, SEND_VALUE*10)
    with boa.env.prank(account.address):
        raffle.fund(value=SEND_VALUE)
    return raffle