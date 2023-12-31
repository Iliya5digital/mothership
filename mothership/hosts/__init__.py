from __future__ import annotations
from typing import (
    Any,
    Optional,
    List,
    Dict,
    Protocol,
    Type,
    ClassVar,
    final,
    Generic,
    TypeVar,
)

from pathlib import Path, PurePosixPath
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from mothership.mount import BASES_PATH, HOSTS_PATH
from mothership.beacon import Reflex


class Dump(Protocol):
    def dump(self) -> Any:
        ...


class Mac:
    def __init__(self, addr: str) -> None:
        parts = addr.split(":")
        assert len(parts) == 6
        self.bytes = bytes([int(p, base=16) for p in parts])

    def __hash__(self) -> int:
        return hash(self.bytes)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Mac):
            raise TypeError(f"`other` must be {Mac}, not {type(other)}")
        return self.bytes == other.bytes

    def __str__(self) -> str:
        return ":".join([f"{b:02x}" for b in self.bytes])

    def __repr__(self) -> str:
        return f"Mac({str(self)})"

    def dump(self) -> str:
        return str(self)


@dataclass
class Base:
    name: str
    parent: Base | None = None
    _path: Path | None = None

    @property
    def path(self) -> Path:
        if self._path is not None:
            return self._path
        else:
            return BASES_PATH / self.name

    def branch(self) -> List[Path]:
        if self.parent is not None:
            base = self.parent.branch()
        else:
            base = []
        return [*base, self.path]


class Status:
    @final
    def _update_reflex(self, reflex: Reflex) -> None:
        now = datetime.now()
        self.addr = reflex.addr
        self.online = now
        self.boot = now - timedelta(seconds=reflex.info.uptime)

    def __init__(self, reflex: Reflex) -> None:
        self.error: Optional[str] = None
        self._update_reflex(reflex)

    async def update(self, reflex: Reflex, force: bool = False) -> None:
        self._update_reflex(reflex)

    def dump(self) -> Dict[str, Any]:
        return {
            "addr": self.addr,
            "boot": int(self.boot.timestamp()),
            "online": int(self.online.timestamp()),
            **({"error": self.error} if self.error is not None else {}),
        }


@final
class OrphanStatus(Status):
    pass


@dataclass
class Host:
    name: str
    mac: Mac
    addr: str | None = None
    base: Base | None = None
    files: Dict[PurePosixPath, str] = field(default_factory=dict)

    @property
    def path(self) -> Path:
        return HOSTS_PATH / str(self.mac) / "merged"

    @classmethod
    def status_classes(cls) -> List[Type[Status]]:
        return [HostStatus]

    @final
    def new_status(self, reflex: Reflex) -> HostStatus:
        ty = type(f"_{type(self).__name__}Status", tuple(self.status_classes()), {})
        return ty(reflex, self)

    def dump(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mac": str(self.mac),
            **({"base": self.base.name} if self.base is not None else {}),
            **({"addr": self.addr} if self.addr is not None else {}),
        }


T = TypeVar("T", bound=Host, covariant=True)


class HostStatus(Status, Generic[T]):
    def __init__(self, reflex: Reflex, host: T, /) -> None:
        super().__init__(reflex)
        self.host = host
