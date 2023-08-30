from pathlib import PurePosixPath as Path

from mothership.hosts import Mac, Base
from mothership.hosts.nand import Nand
from mothership.hosts.ioc import Ioc

debian = Base("debian")
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
    Skifio("mpsc14", Mac("f8:dc:7a:a4:1c:42")),
    Skifio("mpsc15", Mac("f8:dc:7a:a4:1c:60")),
    Skifio("mpsc16", Mac("f8:dc:7a:a4:1c:9c")),
    Skifio("mpsc17", Mac("f8:dc:7a:a4:1c:a6")),
    Skifio("mpsc18", Mac("f8:dc:7a:a4:1c:cc")),
    Skifio("mpsc19", Mac("f8:dc:7a:a4:1c:de")),
    Skifio("mpsc20", Mac("f8:dc:7a:a4:1c:e0")),
    Skifio("mpsc21", Mac("f8:dc:7a:a4:1c:e2")),
    Skifio("mpsc22", Mac("f8:dc:7a:a4:1c:e4")),
    Skifio("mpsc23", Mac("f8:dc:7a:a4:1c:e6")),
    Skifio("mpsc24", Mac("f8:dc:7a:a4:1c:e8")),
    Skifio("mpsc25", Mac("f8:dc:7a:a4:1c:ec")),
    Skifio("mpsc26", Mac("f8:dc:7a:a4:1c:ee")),
    Skifio("mpsc27", Mac("f8:dc:7a:a4:1c:f2")),
    Skifio("mpsc28", Mac("f8:dc:7a:a4:1c:f4")),
    Skifio("mpsc29", Mac("f8:dc:7a:a4:1d:16")),
]
