from __future__ import annotations
from typing import Any, Optional, List, Dict, Type

import asyncio
import json

import asyncssh
from pyepics_asyncio import Pv

from mothership.hosts import Host, Status, HostStatus
from mothership.beacon import Reflex
from .ssh import SSH_KWS


class Ioc(Host):
    def __init__(self, *args: Any, prefix: str, **kws: Any) -> None:
        super().__init__(*args, **kws)
        self.prefix = prefix

    @classmethod
    def status_classes(cls) -> List[Type[Status]]:
        return [_IocStatus, *super().status_classes()]

    def dump(self) -> Dict[str, Any]:
        return {
            **super().dump(),
            "ioc": {"prefix": self.prefix},
        }


class _IocStatus(HostStatus[Ioc]):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

        self.version: Optional[str] = None
        self.build_date: Optional[str] = None

        self.stats: Optional[str] = None

    async def update(self, reflex: Reflex, force: bool = True) -> None:
        await super().update(reflex, force=force)

        try:
            async with asyncio.timeout(4):
                self.version = await (
                    await Pv.connect(f"{self.host.prefix}Version")
                ).get()
                # self.build_date = await (
                #    await Pv.connect(f"{self.host.prefix}BuildDate")
                # ).get()

                async with asyncssh.connect(self.addr, **SSH_KWS) as conn:
                    try:
                        self.stats = json.loads(
                            (
                                await conn.run(
                                    "cat /opt/ioc/iocBoot/iocTornado/stats.json",
                                    check=True,
                                )
                            ).stdout
                        )
                    except RuntimeError:
                        self.stats = None
        except TimeoutError:
            self.version = None
            # self.build_date = None
            self.stats = None

    def dump(self) -> Dict[str, Any]:
        data = super().dump()
        if self.version is not None:
            data["ioc"] = {
                "version": self.version,
                # "build_date": self.build_date,
                "stats": self.stats,
            }
        return data
