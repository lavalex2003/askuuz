from enum import StrEnum

DOMAIN = "askuuz"
PLATFORMS = ["sensor"]


class UtilityType(StrEnum):
    ELECTRICITY = "electricity"
    WATER = "water"
    GAS = "gas"
    MANAGEMENT = "management"
    GARBAGE = "garbage"
