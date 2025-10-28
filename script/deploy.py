from moccasin.config import get_active_network
from moccasin.boa_tools import VyperContract
from script.deploy_mocks import deploy_feed
from src import buy_me_a_coffee

def deploy_coffee(price_feed: str) -> VyperContract:
    coffee: VyperContract =buy_me_a_coffee.deploy(price_feed)

    active_network = get_active_network()
    if active_network.has_explorer():
        result = active_network.moccasin_verify(coffee)
        result.wait_for_verification()
    return coffee

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"On network {active_network.name}, found price feed at {price_feed.address}")
    return deploy_coffee(price_feed)
    # price_feed: VyperContract = deploy_feed()
    # coffee = buy_me_a_coffee.deploy(price_feed.address)
    # print(f"Deployed Coffee contract at {coffee.address} with price feed {price_feed.address} on {active_network.name}")

    # print(coffee.get_eth_to_usd_rate(1000))
    