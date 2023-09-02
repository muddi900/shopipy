from dataclasses import dataclass


@dataclass
class Product:
    body_html: str | None
    created_at: str | None
    handle: str | None
    id: str | None
    images: list[dict] | None
    options: dict | None
    product_type: str | None
    published_at: str | None
    published_scope: str | None
    status: str | None
    tags: str | None
    template_suffix: str | None
    title: str | None
    updated_at: str | None
    variants: list[dict] | None
    vendor: str | None


@dataclass
class ProductImage:
    id: int
    product_id: int
    position: int | None
    created_at: str | None
    updated_at: str | None
    width: int | None
    height: int | None
    src: str | None
    variant_ids: list[dict] | None


@dataclass
class ProductOption:
    id: int
    product_id: int
    name: str | None
    position: int | None
    values: list[str] | None


@dataclass
class ProductVariant:
    barcode: str | None
    compare_at_price: str | None
    created_at: str | None
    fulfillment_service: str | None
    grams: int | None
    weight: float | None
    weight_unit: str | None
    id: int
    inventory_item_id: int | None
    inventory_management: str | None
    inventory_policy: str | None
    inventory_quantity: int | None
    option1: str | None
    position: int | None
    price: float | None
    product_id: int | None
    requires_shipping: bool
    sku: str | None
    taxable: bool
    title: str | None
    updated_at: str | None
