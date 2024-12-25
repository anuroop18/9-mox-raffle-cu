import boa


def test_fund_fails_if_not_enough_eth(raffle):
    with boa.reverts("You must spend more ETH!"):
        raffle.fund()