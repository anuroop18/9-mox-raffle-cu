# pragma version 0.4.0
"""
@license MIT
@title raffle
@author You!
@notice This contract is for creating a raffle
"""

from interfaces import AggregatorV3Interface
import get_price_module

# owner of contract. Will get 20% of all funds.
OWNER: public(immutable(address))
PRICE_FEED: public(immutable(AggregatorV3Interface))

# Storage
funders: public(DynArray[address, 1000])
funder_to_amount_funded: public(HashMap[address, uint256])

participants: public(DynArray[address, 1000])
has_entered: public(HashMap[address, bool]) 

ENTRANCE_FEE: public(constant(uint256)) = as_wei_value(5, "ether")
RAFFLE_DURATION: public(constant(uint256)) = 30
raffle_start_time: public(uint256)

flag RaffleState:
    OPEN
    CALCULATING

@deploy
def __init__(price_feed: address):
    PRICE_FEED = AggregatorV3Interface(price_feed)
    OWNER = msg.sender


@payable
@external
def fund():
    self._fund()


@payable
@internal
def _fund():
    """Allows users to send $ to this contract
    Have a minimum $ amount to send"""

    usd_value_of_eth: uint256 = get_price_module._get_eth_to_usd_rate(
        PRICE_FEED, msg.value
    )
    assert usd_value_of_eth >= ENTRANCE_FEE, "You must spend more ETH!"
    self.funders.append(msg.sender)
    self.funder_to_amount_funded[msg.sender] += msg.value


@payable
@internal
def _distribute_winnings(winner:address):
    pass


# Create a basic Raffle contract
# Add Randomness function

# Now add mock for testing
#


