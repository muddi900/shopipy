from dataclasses import dataclass


@dataclass
class Webhook:
    address: str
    api_version: str
    created_at: str
    fields: list[str]
    format: str
    id: int
    metafield_namespaces: list[str]
    private_metafield_namespaces: list[str]
    topic: str
    updated_at: str
