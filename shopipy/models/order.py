from dataclasses import dataclass
from typing import Any
from fulfillment import Fulfillment
from customer import Customer, Address


@dataclass
class ClientDetails:
    accept_language: str
    browser_height: int
    browser_ip: str
    browser_width: int
    session_hash: str
    user_agent: str


@dataclass
class Company:
    id: int
    location_id: int


@dataclass
class CurrentTotalAdditionalFeesSet:
    shop_money: dict[str, str]
    presentment_money: dict[str, str]


@dataclass
class CurrentTotalDiscountsSet:
    shop_money: dict[str, str]
    presentment_money: dict[str, str]


@dataclass
class CurrentTotalDutiesSet:
    shop_money: dict[str, str]
    presentment_money: dict[str, str]


@dataclass
class CurrentTotalPriceSet:
    shop_money: dict[str, str]
    presentment_money: dict[str, str]


@dataclass
class DiscountApplication:
    type: str
    title: str
    description: str
    value: str
    value_type: str
    allocation_method: str
    target_selection: str
    target_type: str


@dataclass
class DiscountCode:
    code: str
    amount: str
    type: str


@dataclass
class Location:
    id: int
    location_id: int


@dataclass
class OriginalTotalAdditionalFeesSet:
    shop_money: dict[str, str]
    presentment_money: dict[str, str]


@dataclass
class OriginalTotalDutiesSet:
    shop_money: dict[str, str]
    presentment_money: dict[str, str]


@dataclass
class PaymentDetails:
    avs_result_code: str
    credit_card_bin: str
    cvv_result_code: str
    credit_card_number: str
    credit_card_company: str


@dataclass
class PaymentTerms:
    amount: int
    currency: str
    payment_terms_name: str
    payment_terms_type: str
    due_in_days: int
    payment_schedules: list[dict[str, str]]


@dataclass
class ShippingLine:
    code: str
    price: str
    price_set: dict[str, str]
    discounted_price: str
    discounted_price_set: dict[str, str]
    source: str
    title: str
    tax_lines: list[dict[str, str]]
    carrier_identifier: str
    requested_fulfillment_service_id: str


@dataclass
class TaxLine:
    price: str
    rate: float
    title: str
    channel_liable: bool


@dataclass
class Order:
    app_id: int
    billing_address: Address
    browser_ip: str
    buyer_accepts_marketing: bool
    cancel_reason: str
    cancelled_at: str
    cart_token: str
    checkout_token: str
    client_details: ClientDetails
    closed_at: str
    company: Company
    confirmation_number: str
    created_at: str
    currency: str
    current_total_additional_fees_set: Any | CurrentTotalAdditionalFeesSet
    current_total_discounts: str
    current_total_discounts_set: Any | CurrentTotalDiscountsSet
    current_total_duties_set: Any | CurrentTotalDutiesSet
    current_total_price: str
    current_total_price_set: Any | CurrentTotalPriceSet
    current_subtotal_price: str
    current_subtotal_price_set: Any | CurrentTotalPriceSet
    current_total_tax: str
    current_total_tax_set: Any | CurrentTotalPriceSet
    customer: Customer
    customer_locale: str
    discount_applications: dict[str, Any]
    discount_codes: list[DiscountCode] | list[Any]
    email: str
    estimated_taxes: bool
    financial_status: str
    fulfillments: list[Fulfillment]
    fulfillment_status: str
    gateway: str
    id: int
    landing_site: str
    line_items: list[dict[str, Any]]
    location_id: int
    merchant_of_record_app_id: int
    name: str
    note: str
    note_attributes: list[dict[str, Any]]
    number: int
    order_number: int
    original_total_additional_fees_set: OriginalTotalAdditionalFeesSet | dict[Any, Any]
    original_total_duties_set: OriginalTotalDutiesSet | dict[Any, Any]
    payment_details: PaymentDetails | dict[Any, Any]
    payment_terms: PaymentTerms | dict[Any, Any]
    payment_gateway_names: list[str]
    phone: str
    po_number: str
    presentment_currency: str
    processed_at: str
    processing_method: str
    referring_site: str
    refunds: list[dict[str, Any]]
    shipping_address: Address
    shipping_lines: list | list[ShippingLine]
    source_name: str
    source_identifier: str
    source_url: str
    subtotal_price: str
    subtotal_price_set: Any | CurrentTotalPriceSet | None
    tags: str
    tax_lines: list[TaxLine]
    taxes_included: bool
    test: bool
    token: str
    total_discounts: str
    total_discounts_set: Any | CurrentTotalDiscountsSet | None
    total_line_items_price: str
    total_line_items_price_set: Any | CurrentTotalPriceSet | None
    total_outstanding: str
    total_price: str
    total_price_set: Any | CurrentTotalPriceSet
    total_shipping_price_set: Any | CurrentTotalPriceSet
    total_tax: str
    total_tax_set: Any | CurrentTotalPriceSet
    total_tip_received: str
    total_weight: int
    updated_at: str
    user_id: int
    order_status_url: dict[str, str]

    def __post_init__(self):
        # Assign custom classes to specific fields
        self.billing_address = Address(**self.billing_address)
        self.client_details = ClientDetails(**self.client_details)
        self.company = Company(**self.company)
        self.current_total_additional_fees_set = CurrentTotalAdditionalFeesSet(
            **self.current_total_additional_fees_set
        )
        self.current_total_discounts_set = CurrentTotalDiscountsSet(
            **self.current_total_discounts_set
        )
        self.current_total_duties_set = CurrentTotalDutiesSet(
            **self.current_total_duties_set
        )
        self.current_total_price_set = CurrentTotalPriceSet(
            **self.current_total_price_set
        )
        self.customer = Customer(**self.customer)
        self.discount_applications = DiscountApplication(**self.discount_applications)
        self.original_total_additional_fees_set = OriginalTotalAdditionalFeesSet(
            **self.original_total_additional_fees_set
        )
        self.original_total_duties_set = OriginalTotalDutiesSet(
            **self.original_total_duties_set
        )
        self.payment_details = PaymentDetails(**self.payment_details)
        self.payment_terms = PaymentTerms(**self.payment_terms)
        self.shipping_address = Address(**self.shipping_address)
        self.subtotal_price_set = CurrentTotalPriceSet(**self.subtotal_price_set)
        self.total_discounts_set = CurrentTotalDiscountsSet(**self.total_discounts_set)
        self.total_line_items_price_set = CurrentTotalPriceSet(
            **self.total_line_items_price_set
        )
        self.total_price_set = CurrentTotalPriceSet(**self.total_price_set)
        self.total_shipping_price_set = CurrentTotalPriceSet(
            **self.total_shipping_price_set
        )
        self.total_tax_set = CurrentTotalPriceSet(**self.total_tax_set)
