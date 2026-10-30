"""Shared target-scope checks for local cyber-range simulations."""

import ipaddress


def is_allowed_lab_target(target: str) -> bool:
    """Allow IPv4 loopback/private addresses only; reject public and special ranges."""
    try:
        address = ipaddress.ip_address(str(target).strip())
    except ValueError:
        return False

    return (
        address.version == 4
        and (address.is_private or address.is_loopback)
        and not (
            address.is_link_local
            or address.is_multicast
            or address.is_reserved
            or address.is_unspecified
        )
    )


def require_lab_target(target: str) -> str:
    if not is_allowed_lab_target(target):
        raise ValueError(
            "Target must be a private or loopback IPv4 address in your authorised lab."
        )
    return str(ipaddress.ip_address(str(target).strip()))
