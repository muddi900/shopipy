from dataclasses import dataclass


@dataclass
class Address:
    address1: str
    address2: str | None
    city: str
    company: str | None
    country: str
    first_name: str
    last_name: str
    phone: str
    province: str | None
    zip: str
    name: str
    province_code: str | None
    country_code: str | None
    latitude: str | None
    longitude: str | None


@dataclass
class Customer:
    id: int
    email: str
    accepts_marketing: bool
    created_at: str
    updated_at: str
    first_name: str
    last_name: str
    state: str
    note: str
    verified_email: bool
    multipass_identifier: str
    tax_exempt: bool
    tax_exemptions: dict[str, str]
    phone: str
    tags: str
    currency: str
    addresses: dict[str, str | Address]
    admin_graphql_api_id: str
    default_address: dict[str, str] | Address

    def __post_init__(self):
        self.default_address = Address(**self.default_address)
        for k, address in self.addresses.items():
            self.addresses[k] = Address(**address)
