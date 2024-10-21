from .basic import StrEnum


class Disruption(StrEnum):
    """
    An indicator of the level of disruption involved in installing an improvement.
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class InstallationTimeframe(StrEnum):
    """
    An indicator of the time involved in installing an improvement.
    This is the time for works within/around the home, and does not include lead times
    for arranging the works.

    This is only a reference and can not take into account unique complexities of
    individual homes.
    """

    A_DAY = "A day"
    A_FEW_DAYS = "A few days"
    A_WEEK = "A week"
    A_FEW_WEEKS = "A few weeks"


class AdditionalImprovementCategory(StrEnum):
    """
    Additional improvement categories not defined in PAS2035.
    """

    ZUOS_CUSTOM = "Custom ZUoS improvements"


class AdditionalImprovementMeasure(StrEnum):
    """
    Additional improvement measures not defined in PAS2035.
    """

    BATTERY = "Battery"
    WET_UNDER_FLOOR_HEATING = "Wet underfloor heating"


class ImprovementMeasureCompatibility(StrEnum):
    """
    PAS2035 measure compatibility.
    Wording from the PAS2035 compliance risk matrix v9.13.
    """

    NEED_CONSTRUCTION_DETAIL = "need construction detail"
    SPECIFICATION_REQUIRED = "compatible specification required"
    INCOMPATIBLE = "these measures are not compatible"
