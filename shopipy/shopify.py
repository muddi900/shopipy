import os
import asyncio
import httpx

from enum import Enum
from typing import Any


class BulkAction(Enum):
    GET = 1
    CREATE = 2
    EDIT = 3
    DELETE = 4


class Shopify:
    def __init__(
        self,
        store_slug: str,
        *,
        admin_key=os.environ.get("SHOPIFY_ADMIN_KEY", None),
    ) -> None:

        if admin_key is None:
            raise TypeError("Admin key can't be none")
        self.__url = f"https://{store_slug}.myshopify.com/admin/api/2022-07"
        self.__headers = {"X-Shopify-Access-Token": admin_key}

    async def __get_client(self, **kwargs) -> httpx.AsyncClient:
        return await httpx.AsyncClient(headers=self.__headers, **kwargs)

    async def __bulk_request(
        self, action: BulkAction, *, endpoint: str | None, payloads: list[dict]
    ):
        match action:
            case BulkAction.GET:
                runner = self.__get_item
            case BulkAction.CREATE:
                runner = self.__create_items
            case _:
                return

        tasks = []

        for payload in payloads:
            if endpoint is not None and "url_json_path" not in payload:
                payload["url_json_path"] = endpoint

            tasks.append(asyncio.current_task(runner(**payload)))

    async def __get_item(
        self,
        *,
        url_json_path: str,
        limit: int | None,
    ) -> httpx.Response:
        if limit > 250:
            raise AttributeError("The max limit is 250")

        async_client = await self.__get_client()

        url = f"{self.__url}/{url_json_path}"

        if limit is not None or limit > 0:
            url = f"{url}?limit={limit}"
        resp = await async_client.get(url)
        async_client.close()
        return resp

    async def __create_items(
        self,
        *,
        client: httpx.AsyncClient = None,
        url_json_path: str,
        data: dict[Any, Any],
    ) -> httpx.Response:

        url = f"{self.__url}/{url_json_path}"
        if client is None:
            client = await self.__get_client()

        resp = client.post(url, json=data)
        client.close()
        return resp

    async def get_orders(self, limit=50, *, order_id: str | int = None):
        if order_id is not None:
            json_path = f"orders/{order_id}.json"
        else:
            json_path = "orders.json"
            limit = None

        orders = await self.__get_item(url_json_path=json_path, limit=limit)

        return orders.json()

    def get_orders_sync(self, limit=50):
        return asyncio.run(self.get_orders_async(limit))

    async def get_products(self, limit=50, product_id: str | int = None):
        if product_id is None:
            json_path = "products.json"
        else:
            json_path = f"products/{product_id}.json"
            limit = None

        products = await self.__get_item(url_json_path=json_path, limit=limit)

        return products.json()

    def get_products_sync(self, limit=50):
        return asyncio.run(self.get_products(limit))

    async def create_product(self, data: dict[Any, Any]) -> dict:

        resp = await self.__create_items(
            data=data,
            url_json_path="products.json",
        )

        return resp.json()

    def create_product_sync(self, data: dict[Any, Any]) -> dict:
        return asyncio.run(self.create_product(data))

    async def get_users(self):
        resp = await self.__get_item(url_json_path="users.json")

        return resp.a

    def get_users_sync(self):
        return asyncio.run(self.get_users())
