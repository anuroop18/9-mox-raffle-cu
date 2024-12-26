from eth_utils import to_wei
from moccasin.boa_tools import VyperContract

from contracts import raffle

INTERVAL = 100
entrance_fee = to_wei(1, "ether")


def deploy_raffle() -> VyperContract:
    raffle_contract: VyperContract = raffle.deploy(INTERVAL, entrance_fee)
    print(f"Raffle deployed at {raffle_contract.address}")
    # Interact with the contract
    # call enter_raffle for 10 players
    # get contract INTERVAL
    # move block.timestamp forward by INTERVAL
    # get raffle.balance
    # call request_winner
    # old_balance = raffle.balance
    # check if raffle.balance is 0
    # check if recent_winner is not None
    # check if recent_winner.balance  == old_balance
    return raffle_contract

def moccasin_main() -> VyperContract:
    return deploy_raffle()
