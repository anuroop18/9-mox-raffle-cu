from moccasin.boa_tools import VyperContract

from contracts.mocks import mock_v3_aggregator

STARTING_DECIMALS = 8
STARTING_PRICE = int(2000e8)

def deploy_feed() -> VyperContract:
    return mock_v3_aggregator.deploy(STARTING_DECIMALS, STARTING_PRICE)

def moccasin_main() -> VyperContract:
    return deploy_feed()