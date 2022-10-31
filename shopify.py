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
        self.__url = f"https://{store_slug}.myshopify.com/admin/api/2022-07/"
        self.__headers = {"X-Shopify-Access-Token": admin_key}

    async def get_orders_async(self, limit=50):
        async with httpx.AsyncClient(headers=self.__headers) as client:
            orders = await client.get(f"{self.__url}/orders.json?limit={limit}")

        return orders.json()

    def get_orders(self, limit=50):
        return asyncio.run(self.get_orders_async(limit))
