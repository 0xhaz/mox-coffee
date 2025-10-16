from src.mocks import MockV3Aggregator
from moccasin.boa_tools import VyperContract
from script.deploy_mocks import deploy_feed

STARTING_DECIMALS = 8
STARTING_PRICE = int(2000e8)



def deploy_feed() -> VyperContract:
    mock_v3_aggregator = MockV3Aggregator.deploy(
        STARTING_DECIMALS, STARTING_PRICE
    )

def moccasin_main():
    deploy_feed()