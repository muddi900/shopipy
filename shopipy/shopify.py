import os
import asyncio
import httpx

from enum import Enum
from typing import Any

from models import Order, Product, Customer, Fulfillment, Webhook


class BulkAction(Enum):
    GET = 1
    CREATE = 2
    EDIT = 3
    DELETE = 4


class ReturnMode(Enum):
    DICT = 0
    MODEL = 2


class Shopify:
    """The Main class for the Api. This will be the entry point for our SDK"""

    def __init__(
        self,
        store_slug: str,
        *,
        admin_key=os.environ.get("SHOPIFY_ADMIN_KEY", None),
    ) -> None:
        """
        The API requires a authorized Admin key,
        and the store admin url slug. Admin key can be accessed
        via the App dev panel if your are creating a standalone app.

        Otherwise it requires Oauth flow.
        """

        if admin_key is None:
            raise TypeError("Admin key can't be none")
        self.__url = f"https://{store_slug}.myshopify.com/admin/api/2022-07"
        self.__headers = {"X-Shopify-Access-Token": admin_key}

    def __get_client(self, **kwargs) -> httpx.AsyncClient:
        return httpx.AsyncClient(headers=self.__headers, **kwargs)

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

        client = self.__get_client()

        for payload in payloads:
            if endpoint is not None and "url_json_path" not in payload:
                payload["url_json_path"] = endpoint

            tasks.append(asyncio.current_task(runner(client=client, **payload)))

        await client.aclose()
        return await asyncio.gather(*tasks)

    async def __get_item(
        self,
        *,
        client: httpx.AsyncClient = None,
        url_json_path: str,
        limit: int | None,
        **params,
    ) -> httpx.Response:
        """
        The generic function to get items
        """
        if limit > 250:
            raise AttributeError("The max limit is 250")

        if client is None:
            client = await self.__get_client()

        url = f"{self.__url}/{url_json_path}"

        if limit is not None or limit > 0:
            params = {**params, "limit": limit}
        resp = await client.get(url, params=params)
        await client.aclose()
        return resp

    async def __create_items(
        self,
        *,
        client: httpx.AsyncClient = None,
        url_json_path: str,
        data: dict[Any, Any],
    ) -> httpx.Response:
        """
        The generic function to create items
        """
        url = f"{self.__url}/{url_json_path}"
        if client is None:
            client = await self.__get_client()

        resp = client.post(url, json=data)
        await client.aclose()
        return resp

    async def get_orders(
        self,
        limit=50,
        *,
        order_id: str | int | None = None,
        return_mode: ReturnMode = ReturnMode.DICT,
        **params,
    ) -> list[dict | Order]:
        """
        The method to get orders
        """

        if id is None:
            json_path = "orders.json"
        else:
            json_path = f"orders/{order_id}.json"

        orders = await self.__get_item(url_json_path=json_path, limit=limit, **params)

        if return_mode == 1:
            return [Order(o) for o in orders.json()["Orders"]]

        return orders.json()["orders"]

    def get_orders_sync(
        self,
        limit: int = 50,
        *,
        order_id: str | int | None = None,
        return_mode: ReturnMode = ReturnMode.DICT,
        **params,
    ) -> list[dict | Order]:
        """
        Synchronus vesion of `get_orders`
        """
        return asyncio.run(
            self.get_orders_async(
                limit,
                return_mode=return_mode,
                order_id=order_id,
                **params,
            )
        )

    async def get_products(
        self,
        limit=50,
        *,
        return_mode=ReturnMode.DICT,
        product_id: int | str | None,
        **params,
    ) -> list[dict | Product]:

        """
        Get products from the api,
        """

        if product_id is None:
            json_path = "products.json"
        else:
            json_path = f"products/{product_id}.json"
        limit = None

        products = await self.__get_item(url_json_path=json_path, limit=limit)

        if return_mode == 1:
            return [Product(p) for p in products.json()["products"]]

        return products.json()["products"]

    def get_products_sync(
        self, limit=50, *, product_id=None, return_mode=ReturnMode.DICT, **params
    ) -> list(dict | Product):
        """
        Sync version of `get_products`
        """
        return asyncio.run(
            self.get_products(
                limit,
                return_mode=return_mode,
                product_id=product_id,
                **params,
            ),
        )

    async def create_product(self, data: dict[Any, Any]) -> dict:

        """
        Create a product
        """

        resp = await self.__create_items(
            data=data,
            url_json_path="products.json",
        )

        return resp.json()

    def create_product_sync(self, data: dict[Any, Any]) -> dict:
        """
        Sync version of `create_product`
        """
        return asyncio.run(self.create_product(data))

    async def get_customers(
        self,
        limit=50,
        *,
        return_mode=ReturnMode.DICT,
        customer_id: int | str | None = None,
        **params,
    ) -> list[dict | Customer]:
        """
        Get Customer info.
        """
        if customer_id is None:
            json_path = "customers.json"
        else:
            json_path = f"customers/{customer_id}.json"

        resp = await self.__get_item(url_json_path=json_path, limit=limit, **params)

        if return_mode == 1:
            return [Customer(c) for c in resp.json()["customers"]]

        return resp.json()["customers"]

    def get_customers_sync(
        self,
        limit=50,
        *,
        customer_id=None,
        return_mode: ReturnMode = ReturnMode.DICT,
        **params,
    ) -> list[dict | Customer]:
        """
        Sync version of getting customers.
        """
        return asyncio.run(
            self.get_customers(
                limit,
                return_mode=return_mode,
                customer_id=customer_id,
                **params,
            )
        )

    async def get_webhooks(
        self,
        limit=50,
        *,
        webhook_id: str | int | None = None,
        return_mode: ReturnMode.DICT,
        **params,
    ) -> dict | list[dict] | Webhook | list[Webhook]:
        """
        Get existing webhooks
        """

        # fmt:off
        json_path = "webhooks.json" if webhook_id is None else f"webhooks/{webhook_id}.json"
        # fmt:on
        resp = await self.__get_item(url_json_path=json_path, limit=50, **params)

        resp_data = resp.json()
        if return_mode == 1:
            return (
                [Webhook(w) for w in resp_data["webhooks"]]
                if webhook_id is None
                else Webhook(resp_data["webhook"])
            )
        return resp_data["webhooks"] if webhook_id is None else resp_data["webhook"]

    async def get_fulfillments(
        self,
        limit=50,
        *,
        fullfilment_id: str | int | None = None,
        return_mode: ReturnMode = ReturnMode.DICT,
        params: dict = {},
        **kwargs,
    ) -> list[dict | Fulfillment] | Fulfillment | dict:

        """
        A method to get fulfillments or an individual fulfillment.
        Invidual fulfillments require an order_id to be passed as a kwarg.
        Unlike other get methods, url params need to passed off as a dict.

        TODO: Fetch fulfillment from a FulFillmentOrder
        """
        oid = kwargs.get("order_id")

        if fullfilment_id is None:
            if oid is None:
                json_path = "fulfillments.json"
            else:
                json_path = f"orders/{oid}/fulfillments.json"
        elif oid is None:
            raise AttributeError(
                "Order ID is required to fetch individual fulfillments"
            )

        else:
            json_path = f"orders/{oid}/fulfillments/{fullfilment_id}.json"

        resp = await self.__get_item(url_json_path=json_path, limit=limit, **params)

        if return_mode == 1:
            if fullfilment_id:
                return Fulfillment(resp.json()["fulfillment"])
            return [Fulfillment(f) for f in resp.json()["fulfillments"]]
        elif fullfilment_id is None:
            return resp.json()["fulfillment"]

        return resp.json()["fulfillments"]

    def get_fulfillments_sync(
        self,
        limit=50,
        *,
        fullfilment_id: str | int | None = None,
        return_mode: ReturnMode = ReturnMode.DICT,
        params: dict = {},
        **kwargs,
    ) -> list[dict | Fulfillment] | Fulfillment | dict:
        return asyncio.run(
            self.get_fulfillments(
                limit,
                fullfilment_id=fullfilment_id,
                params=params,
                return_mode=return_mode,
                **kwargs,
            )
        )
