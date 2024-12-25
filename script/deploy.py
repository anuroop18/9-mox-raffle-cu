from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

from contracts import raffle

# from boa.contracts.vyper.vyper_contract import VyperContract

def deploy_raffle(price_feed: VyperContract) -> VyperContract:
    raffle_contract: VyperContract = raffle.deploy(price_feed)
    print(f"Raffle deployed at {raffle_contract.address}")
    return raffle_contract

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"On network {active_network.name}, using price feed at {price_feed.address}")
    return deploy_raffle(price_feed)
