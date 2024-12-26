# Layout of Contract:
# version ✅
# imports
# errors
# Type declarations
# State variables
# Events
# Functions

# Layout of Functions:
# constructor
# receive function (if exists)
# fallback function (if exists)
# external
# public
# internal
# private
# view & pure functions


# pragma version 0.4.0
"""
@license MIT
@title raffle
@author You!
@notice This contract is for creating a raffle
"""

# Imports
from . import auth as ow

initializes: ow
exports: ow.__interface__

# Errors
ERROR_RAFFLE_NOT_OVER: constant(String[100]) = "Raffle: Has not finished"
ERROR_TRANSFER_FAILED: constant(String[100]) = "Raffle: Transfer failed"
ERROR_SEND_MORE_TO_ENTER_RAFFLE: constant(
    String[100]
) = "Raffle: Send more to enter"
ERROR_RAFFLE_NOT_OPEN: constant(String[100]) = "Raffle: Raffle not open"

# State variables
## Constants
MAX_ARRAY_SIZE: constant(uint256) = 1
MAX_NUMBER_OF_PLAYERS: constant(uint256) = 1000

# Immutables
INTERVAL: immutable(uint256)

# Storage variables
entrance_fee: public(uint256)
last_timestamp: public(uint256)
recent_winner: public(address)
players: public(DynArray[address, MAX_NUMBER_OF_PLAYERS])

# Events
event RequestedRaffleWinner:
    request_id: indexed(uint256)


event RaffleEntered:
    player: indexed(address)


event WinnerPicked:
    player: indexed(address)


# Constructor
@deploy
def __init__(interval: uint256, entrance_fee: uint256):
    ow.__init__()
    INTERVAL = interval
    self.entrance_fee = entrance_fee
    self.last_timestamp = block.timestamp


# External functions
@external
def set_fee(new_fee: uint256):
    ow._check_owner()
    self.entrance_fee = new_fee


@external
def get_owner() -> address:
    return ow.owner


@payable
@external
def enter_raffle():
    assert (msg.value >= self.entrance_fee), ERROR_SEND_MORE_TO_ENTER_RAFFLE
    self.players.append(msg.sender)
    log RaffleEntered(msg.sender)


@external
def request_winner():
    raffle_is_ready: bool = self._is_ready_to_request()
    assert raffle_is_ready, ERROR_RAFFLE_NOT_OVER

    index_of_winner: uint256 = convert(
        keccak256(concat(block.prevrandao, convert(block.timestamp, bytes32))),
        uint256,
    ) % len(self.players)
    recent_winner: address = self.players[index_of_winner]
    self.recent_winner = recent_winner
    self.players = []
    self.last_timestamp = block.timestamp
    raw_call(recent_winner, b"", value=self.balance)
    log WinnerPicked(recent_winner)


@view
@external
def is_ready_to_request() -> bool:
    return self._is_ready_to_request()


@view
@external
def get_players() -> DynArray[address, MAX_NUMBER_OF_PLAYERS]:
    return self.players


@view
@internal
def _is_ready_to_request() -> bool:
    time_passed: bool = (block.timestamp - self.last_timestamp) > INTERVAL
    has_players: bool = len(self.players) > 0
    has_balance: bool = self.balance > 0
    raffle_over: bool = time_passed and has_players and has_balance
    return raffle_over
