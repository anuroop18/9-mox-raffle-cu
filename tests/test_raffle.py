import boa
from eth_utils import to_wei
from moccasin.config import get_active_network


# Constructor & initial state tests
def test_constructor_sets_entrance_fee(raffle):
    active_network = get_active_network()
    params = active_network.extra_data
    assert raffle.entrance_fee() == int(params["entrance_fee"])

def test_initial_players_array_is_empty(raffle):
    assert raffle.get_players() == []

# Owner function tests
def test_owner_can_change_fees(raffle, owner):
    new_fee = to_wei(2, "ether")
    assert raffle.entrance_fee() != new_fee
    with boa.env.prank(owner):
        raffle.set_fee(new_fee)
    assert raffle.entrance_fee() == new_fee

def test_user_cannot_change_fees(raffle, user):
    new_fee = to_wei(2, "ether")
    assert raffle.entrance_fee() != new_fee
    with boa.reverts("ownable: caller is not the owner"):
        with boa.env.prank(user):
            raffle.set_fee(new_fee)

# Raffle function tests
def test_raffle_succeeds_when_you_pay_correct_fee(raffle, user):
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    assert raffle.players(0) == user

def test_raffle_reverts_when_you_pay_less_than_fee(raffle, user):
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        with boa.reverts("Raffle: Send more to enter"):
            raffle.enter_raffle(value=raffle_entrance_fee-1)

def test_multiple_players_can_enter_raffle(raffle):
    raffle_entrance_fee = raffle.entrance_fee()
    num_players: int = 10
    for i in range(num_players):
        player_address = boa.env.generate_address(f"player-{i}")
        boa.env.set_balance(player_address, raffle_entrance_fee*10)
        with boa.env.prank(player_address):
            raffle.enter_raffle(value=raffle_entrance_fee)
            assert raffle.players(i) == player_address

def test_raffle_entered_event_is_emitted(raffle, user):
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    assert raffle.get_logs()[0].topics[0] == user


def test_get_owner_returns_owner(raffle, owner):
    assert raffle.get_owner() == owner

def test_get_players_returns_players(raffle, user):
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    assert raffle.get_players() == [user]

def test_raffle_is_ready_to_request_returns_true_when_ready(raffle, user):
    raffle_entrance_fee = raffle.entrance_fee()
    # add player also sends some ether
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    # move block.timestamp forward by INTERVAL
    boa.env.time_travel(blocks=100)
    assert raffle.is_ready_to_request()

def test_raffle_is_ready_to_request_returns_false_when_no_players(raffle):
    assert not raffle.is_ready_to_request()

def test_request_winner_reverts_when_not_ready(raffle):
    is_ready_to_request = raffle.is_ready_to_request()
    assert not is_ready_to_request
    with boa.reverts("Raffle: Has not finished"):
        raffle.request_winner()

def test_request_winner_adds_winner_to_recent_winner_and_clears_players_array(raffle, user):
    active_network = get_active_network()
    params = active_network.extra_data
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    boa.env.time_travel(seconds=params["interval"]+1)
    assert raffle.is_ready_to_request()
    raffle.request_winner()
    assert raffle.recent_winner() == user
    assert raffle.get_players() == []


def test_request_winner_emits_event_when_winner_picked(raffle, user):
    active_network = get_active_network()
    params = active_network.extra_data
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    boa.env.time_travel(seconds=params["interval"]+1)
    assert raffle.is_ready_to_request()
    raffle.request_winner()
    print(raffle.get_logs())
    assert raffle.get_logs()[0].topics[0] == user

def test_balance_of_raffle_is_zero_after_winner_picked(raffle, user):
    active_network = get_active_network()
    params = active_network.extra_data
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    boa.env.time_travel(seconds=params["interval"]+1)
    assert raffle.is_ready_to_request()
    raffle.request_winner()
    assert boa.env.get_balance(raffle.address) == 0

def test_winner_balance_is_equal_to_raffle_balance(raffle, user):
    active_network = get_active_network()
    params = active_network.extra_data
    raffle_entrance_fee = raffle.entrance_fee()
    with boa.env.prank(user):
        raffle.enter_raffle(value=raffle_entrance_fee)
    boa.env.time_travel(seconds=params["interval"]+1)
    assert raffle.is_ready_to_request()
    user_balance_old = boa.env.get_balance(user)
    raffle.request_winner()
    user_balance_new = boa.env.get_balance(user)
    assert user_balance_new == user_balance_old + raffle_entrance_fee