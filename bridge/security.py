"""Small, dependency-free network and bearer-token checks for the bridge."""

from __future__ import annotations

import hmac
import ipaddress


def validate_binding(host: str, api_key: str) -> None:
    if host.lower() == "localhost":
        loopback = True
    else:
        try:
            loopback = ipaddress.ip_address(host).is_loopback
        except ValueError as exc:
            raise ValueError("BRIDGE_HOST must be localhost or an IP address") from exc
    if not loopback and not api_key:
        raise ValueError("BRIDGE_API_KEY is required when BRIDGE_HOST is not loopback")


def authorized(header: str, api_key: str) -> bool:
    if not api_key:
        return True
    if not header.startswith("Bearer "):
        return False
    return hmac.compare_digest(header[7:], api_key)
