from enum import Enum

class PlatformType(str, Enum):
    SOURCING = "sourcing"
    CONSIGNMENT = "consignment"
    OVERSEAS = "overseas"
    VERTICAL = "vertical"
    STORE = "store"
