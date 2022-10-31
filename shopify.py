import os
import asyncio
import httpx


class Shopify:
    def __init__(
        self,
        store_slug: str,
        admin_key=os.environ.get("SHOPIFY_ADMIN_KEY", None),
    ) -> None:

        if admin_key is None:
            raise TypeError("Admin key can't be none")
        self.__url = f"https://{store_slug}.myshopify.com"


    def 