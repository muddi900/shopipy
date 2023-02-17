import vcr
import httpx


@vcr.use_cassette()
def test_order_resp(resp) -> None:
    