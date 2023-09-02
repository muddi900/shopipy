import vcr
import httpx
from shopipy import Shopify


@vcr.use_cassette()
def test_order_resp() -> None:
    s = Shopify("url_slug")
    pass
