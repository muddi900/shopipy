import os
import asyncio
import httpx

from typing import Any


class Shopify:
    def __init__(
        self,
        store_slug: str,
        admin_key=os.environ.get("SHOPIFY_ADMIN_KEY", None),
    ) -> None:

        if admin_key is None:
            raise TypeError("Admin key can't be none")
        self.__url = f"https://{store_slug}.myshopify.com/admin/api/2022-07"
        self.__headers = {"X-Shopify-Access-Token": admin_key}

    async def __get_item(
        self,
        *,
        url_json_path: str,
        async_client: httpx.AsyncClient,
        limit: int | None,
    ) -> httpx.Response:
        if limit > 250:
            raise AttributeError("The max limit is 250")

        url = f"{self.__url}/{url_json_path}"

        if limit is not None or limit > 0:
            url = f"{url}?limit={limit}"
        return await async_client.get(url)

    async def __create_items(
        self,
        *,
        url_json_path: str,
        client: httpx.AsyncClient,
        limit: int | None,
        data: dict[Any, Any],
    ) -> httpx.Response:

        url = f"{self.__url}/{url_json_path}"

        return client.post(url, json=data)

    async def get_orders(self, limit=50, *, order_id: str | int = None):
        async with httpx.AsyncClient(headers=self.__headers) as client:
            orders = await self.__get_item(
                url_json_path="orders.json",
                async_client=client,
                limit=limit,
            )

        return orders.json()

    def get_orders_sync(self, limit=50):
        return asyncio.run(self.get_orders_async(limit))

    async def get_products(self, limit=50):
        async with httpx.AsyncClient(headers=self.__headers) as client:
            products = await self.__get_item(
                url_json_path="products.json",
                async_client=client,
                limit=limit,
            )

        return products.json()

    def get_products_sync(self, limit=50):
        return asyncio.run(self.get_products(limit))

    async def create_product(self, data: dict[Any, Any]) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await self.__create_items(
                data=data,
                client=client,
                url_json_path="products.json",
            )

        return resp.json()

    def create_product_sync(self, data: dict[Any, Any]) -> dict:
        return asyncio.run(self.create_product(data))
