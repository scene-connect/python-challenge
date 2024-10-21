import logging

from .basic import StrEnum

log = logging.getLogger(__name__)


class InsulationMaterial(StrEnum):
    """
    Materials used for insulation.
    Source: SAP10 Table 14
    """

    MINERAL_WOOL = "mineral wool"
    ROCK_WOOL = "rock wool"
    FIBRE_GLASS = "fibre glass"
    EPS = "EPS (expanded polystyrene)"
    XPS = "XPS (extruded polystyrene)"
    PUR = "PUR (polyurethene foam)"
    PIR = "PIR (polyisocyanurate)"
    PHENOLIC_FOAM = "phenolic foam"


class DomesticEnergyEndUse(StrEnum):
    """
    Domestic energy end use categories, based on groupings of ECUK categories.
    """

    SPACE_HEATING = "Space heating"
    HOT_WATER = "Hot water"
    LIGHTING = "Lighting"
    COOKING = "Cooking"
    COLD_AND_WET_APPLIANCES = "Cold and wet appliances"
    ELECTRONICS_AND_OTHER = "Electronics and other"


class EnergySource(StrEnum):
    """
    Energy sources.
    Mirrors and expands fuel types from zuos_types.epcs.enums.HeatingSystemEnergySource
    """

    # Values matching zuos_types.epcs.enums.HeatingSystemEnergySource
    B30K = "B30K"
    BIOETHANOL = "bioethanol"
    BOTTLED_LPG = "bottled LPG"
    COAL = "coal"
    DUAL_FUEL_MINERAL_WOOD = "dual fuel (mineral and wood)"
    ELECTRIC = "electric"
    LIQUID_BIOFUEL = "liquid biofuel"
    LNG = "LNG"
    LPG = "LPG"
    MAINS_GAS = "mains gas"
    OIL = "oil"
    RAPESEED_OIL = "rapeseed oil"
    SMOKELESS_FUEL = "smokeless fuel"
    WOOD_CHIPS = "wood chips"
    WOOD_LOGS = "wood logs"
    WOOD_PELLETS = "wood pellets"

    # Additional values, mostly added from
    # zuos_types.elmhurst.rdsap_report.HeatingFuelTypeCode
    ANTHRACITE = "anthracite"
    # Deprecated in HeatingFuelTypeCode but present for compatibility.
    BIOMASS = "biomass"
    BIOGAS = "biogas"
    B30D = "B30D"

    @property
    def is_gas(self) -> bool:
        return self in (
            self.BOTTLED_LPG,
            self.MAINS_GAS,
            self.LNG,
            self.LPG,
        )

    @property
    def is_oil(self) -> bool:
        return self in (
            self.B30K,
            self.OIL,
            self.RAPESEED_OIL,
            self.BIOETHANOL,
            self.LIQUID_BIOFUEL,
        )

    @property
    def is_solid(self) -> bool:
        return self in (
            self.COAL,
            self.DUAL_FUEL_MINERAL_WOOD,
            self.SMOKELESS_FUEL,
            self.WOOD_CHIPS,
            self.WOOD_PELLETS,
            self.WOOD_LOGS,
        )


class FloorInsulationPosition(StrEnum):
    ABOVE_SLAB = "Above Slab"
    AT_JOISTS = "At Joists"
    BETWEEN_JOISTS = "Between Joists"


class RoofInsulationPosition(StrEnum):
    BETWEEN_JOISTS = "Unknown, Between Joists"
    AT_RAFTERS = "At Rafters"
    FLAT_ROOF = "Flat Roof Insulation"


class WindowGlazingType(StrEnum):
    DOUBLE_GLAZING = "double glazing"
    TRIPLE_GLAZING = "triple glazing"
    SECONDARY_GLAZING = "secondary glazing"
    SINGLE_GLAZING = "single glazing"
    NOT_DEFINED = "not defined"


class WindowConstruction(StrEnum):
    PVC = "PVC"
    WOOD = "Wood"
    METAL = "Metal"


class WindowGlazingGap(StrEnum):
    SMALL = 6
    MEDIUM = 12
    LARGE = "16 or more"
