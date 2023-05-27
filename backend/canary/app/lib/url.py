from asyncio import wait_for
from ipaddress import ip_address
from typing import TYPE_CHECKING, List, Literal, Union

import aiodns
import yarl
from aiohttp import ClientResponse, ClientTimeout
from aiohttp_proxy import ProxyConnector
from app.errors import LocalDomainInvalid
from env import SETTINGS

if TYPE_CHECKING:
    from app.types import State


async def untrusted_http_request(
    state: "State",
    url: str,
    method: Union[Literal["GET"], Literal["POST"], Literal["DELETE"], Literal["PUT"]],
    **kwargs
) -> ClientResponse:
    try:
        await is_local(
            url,
            # If no proxy, then try our best to
            # ensure the request doesn't resolve to a local IP.
            attempt_dns_resolve=not SETTINGS.untrusted_request_proxy,
        )
    except LocalDomainInvalid:
        raise

    if SETTINGS.untrusted_request_proxy:
        kwargs["connector"] = ProxyConnector.from_url(SETTINGS.untrusted_request_proxy)

    # Don't allow redirects
    kwargs["allow_redirects"] = False
    kwargs["timeout"] = ClientTimeout(total=30.0)
    return await wait_for(
        state.aiohttp.request(method=method, url=url, **kwargs),
        # Use wait for timeout to ensure request doesn't
        # last longer then 60 seconds, no matter how aiohttp
        # internals handles their timeout.
        60.0,
    )


def __is_local_ip(not_trusted_ip: str) -> bool:
    ip = ip_address(not_trusted_ip)
    return ip.is_loopback or ip.is_private


async def get_localhost_aliases(resolver: aiodns.DNSResolver) -> List[str]:
    aliases = []
    for ip in ("127.0.0.1", "::1"):
        try:
            hostname = await resolver.gethostbyaddr(ip)
            aliases.append(hostname.name)
            aliases.extend(hostname.aliases)
        except aiodns.error.DNSError:
            raise

    return aliases


async def is_local(url: str, attempt_dns_resolve: bool = True) -> None:
    """Used to validate webhooks if it's a local ip or not.

    Raises:
        LocalDomainInvalid
    """

    url_ = yarl.URL(url)

    if url_.scheme not in ("https", "http"):
        raise LocalDomainInvalid()

    domain = url_.host

    if not domain:
        raise LocalDomainInvalid()

    # Check if given domain is an IP
    try:
        if __is_local_ip(domain):
            raise LocalDomainInvalid()
    except ValueError:
        pass

    resolver = aiodns.DNSResolver()

    # Check localhost aliases despite attempt_dns_resolve
    localhost_aliases = await get_localhost_aliases(resolver)
    if domain in localhost_aliases:
        raise LocalDomainInvalid()

    if attempt_dns_resolve:
        try:
            ipv4_address = await resolver.query(domain, "A")
            for ipv4 in ipv4_address:
                if ipv4 in localhost_aliases or __is_local_ip(ipv4):
                    raise LocalDomainInvalid()

            ipv6_address = await resolver.query(domain, "AAAA")
            for ipv6 in ipv6_address:
                if ipv6 in localhost_aliases or __is_local_ip(ipv6):
                    raise LocalDomainInvalid()
        except (aiodns.error.DNSError, ValueError):
            raise LocalDomainInvalid()  # Look up fails, assume is private.