from pathlib import PurePosixPath as Path

from mothership.hosts import Mac, Base, Host
from mothership.hosts.nand import Nand
from mothership.hosts.ioc import Ioc

debian = Base("debian")
tornado = Base("tornado", debian)
skifio = Base("skifio", debian)


class Skifio(Ioc, Nand):
    def __init__(self, name: str, mac: Mac) -> None:
        super().__init__(
            name,
            mac,
            base=skifio,
            files={Path("/opt/env.sh"): f"export DEV_NAME={name}\n"},
            bootloader="U-Boot SPL 2020.04-49381-ged2486e7d2 (Jul 27 2023 - 10:33:36 +0700)",
            fw_env_hash="d73fc4f676c7d1388cb5da50a13f02af54bf0f1b5683abdff9e62248a8c4d91a",
            prefix=f"{name}:",
        )
        self.name = name


hosts = [
    Host("tornado0", Mac("f8:dc:7a:46:04:58"), base=tornado),
    Skifio("mpsc13", Mac("f8:dc:7a:a4:1b:34")),
]
