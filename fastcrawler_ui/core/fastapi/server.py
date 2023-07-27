import asyncio
import os
import ssl
from typing import Any, Awaitable, Callable, Literal, Type

import uvicorn
from fastcrawler import FastCrawler
from pydantic import BaseModel
from uvicorn.config import LOGGING_CONFIG, SSL_PROTOCOL_VERSION, Config


class UvicornConfig(BaseModel):
    app: Callable | str
    host: str = "127.0.0.1"
    port: int = 8000
    uds: str | None = None
    fd: int | None = None
    loop: Literal["none", "auto", "asyncio", "uvloop"] = "asyncio"
    http: Type[asyncio.Protocol] | Literal["auto", "h11", "httptools"] = "auto"
    ws: Type[asyncio.Protocol] | Literal["auto", "none", "websockets", "wsproto"] = "auto"
    ws_max_size: int = 16 * 1024 * 1024
    ws_ping_interval: float | None = 20.0
    ws_ping_timeout: float | None = 20.0
    ws_per_message_deflate: bool = True
    lifespan: Literal["auto", "on", "off"] = "auto"
    env_file: str | os.PathLike | None = None
    log_config: dict[str, Any] | str | None = LOGGING_CONFIG
    log_level: str | int | None = None
    access_log: bool = True
    use_colors: bool | None = None
    interface: Literal["auto", "asgi3", "asgi2", "wsgi"] = "auto"
    reload: bool = False
    reload_dirs: list[str] | str | None = None
    reload_delay: float = 0.25
    reload_includes: list[str] | str | None = None
    reload_excludes: list[str] | str | None = None
    workers: int | None = None
    proxy_headers: bool = True
    server_header: bool = True
    date_header: bool = True
    forwarded_allow_ips: list[str] | str | None = None
    root_path: str = ""
    limit_concurrency: int | None = None
    limit_max_requests: int | None = None
    backlog: int = 2048
    timeout_keep_alive: int = 5
    timeout_notify: int = 30
    timeout_graceful_shutdown: int | None = None
    callback_notify: Callable[..., Awaitable[None]] | None = None
    ssl_keyfile: str | None = None
    ssl_certfile: str | os.PathLike | None = None
    ssl_keyfile_password: str | None = None
    ssl_version: int = SSL_PROTOCOL_VERSION
    ssl_cert_reqs: int = ssl.CERT_NONE
    ssl_ca_certs: str | None = None
    ssl_ciphers: str = "TLSv1"
    headers: list[tuple[str, str]] | None = None
    factory: bool = False
    h11_max_incomplete_event_size: int | None = None

    def generate_config(self) -> Config:
        return Config(**self.model_dump())


class UvicornServer(uvicorn.Server):
    crawler: FastCrawler
    """Customized uvicorn.Server
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    async def handle_exit_async(self, sig: int, frame) -> None:
        await self.crawler._shutdown()

    def handle_exit(self, sig: int, frame) -> None:
        asyncio.ensure_future(self.handle_exit_async(sig, frame))
        return super().handle_exit(sig, frame)
