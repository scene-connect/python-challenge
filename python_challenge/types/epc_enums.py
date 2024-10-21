import functools
import re
from abc import ABC
from abc import ABCMeta
from abc import abstractmethod
from enum import EnumMeta
from enum import IntEnum
from typing import Final

from .basic import PARK_HOME
from .basic import EmptyRange
from .basic import StrEnum
from .basic import T_ParkHome
from .basic import YearRange


class EPCCountry(StrEnum):
    ENGLAND_AND_WALES = "England and Wales"
    NORTHERN_IRELAND = "Northern Ireland"
    SCOTLAND = "Scotland"

    @classmethod
    def from_rdsap_xml(cls, value: str) -> "EPCCountry | None":
        match value:
            case "EAW":
                return cls.ENGLAND_AND_WALES
            case "SCT":
                return cls.SCOTLAND
            case "NIR":
                return cls.NORTHERN_IRELAND
            case _:
                return None


class ImprovementType(StrEnum):
    ADDITIONAL_80_MM_JACKET_TO_HOT_WATER_CYLINDER = (
        "add additional 80mm jacket to hot water cylinder"
    )
    AIR_OR_GROUND_SOURCE_HEAT_PUMP = "air or ground source heat pump"
    AIR_OR_GROUND_SOURCE_HEAT_PUMP_WITH_UNDERFLOOR_HEATING = (
        "air or ground source heat pump with underfloor heating"
    )

    BIOMASS_BOILER = "replace boiler with biomass boiler"
    BOILER_FLUE_GAS_HEAT_RECOVERY = (
        "flue gas heat recovery device in conjunction with boiler"
    )

    CAVITY_WALL_INSULATION = "cavity wall insulation"
    CONDENSING_BOILER = "condensing boiler"
    DOUBLE_GLAZING = "replace single glazed windows with low-E double glazed windows"
    DRAUGHTPROOFING = "draughtproofing"
    FAN_ASSISTED_STORAGE_HEATERS = "fan-assisted storage heaters"
    FAN_ASSISTED_STORAGE_HEATERS_AND_DUAL_IMMERSION_CYLINDER = (
        "fan-assisted storage heaters and dual immersion cylinder"
    )
    FLAT_ROOF_INSULATION = "flat roof insulation"
    FLOOR_INSULATION = "floor insulation"
    FLOOR_INSULATION_SOLID_FLOOR = "floor insulation (solid floor)"
    FLOOR_INSULATION_SUSPENDED_FLOOR = "floor insulation (suspended floor)"
    GAS_CONDENSING_BOILER = "change heating to gas condensing boiler"
    HIGH_HEAT_RETENTION_STORAGE_HEATERS = "high heat retention storage heaters"
    HIGH_HEAT_RETENTION_STORAGE_HEATERS_AND_DUAL_IMMERSION_CYLINDER = (
        "high heat retention storage heaters and dual immersion cylinder"
    )
    HIGH_PERFORMANCE_EXTERNAL_DOORS = "high performance external doors"
    HOT_WATER_CYLINDER_THERMOSTAT = "hot water cylinder thermostat"
    INCREASE_HOT_WATER_CYLINDER_INSULATION = "increase hot water cylinder insulation"
    INCREASE_LOFT_INSULATION_TO_270_MM = "increase loft insulation to 270mm"
    INSULATE_HOT_WATER_CYLINDER_WITH_80_MM_JACKET = (
        "insulate hot water cylinder with 80mm jacket"
    )
    INTERNAL_OR_EXTERNAL_WALL_INSULATION = "internal or external wall insulation"
    LOW_ENERGY_LIGHTING = "low energy lighting for all fixed outlets"
    MIXER_SHOWER_HEAT_RECOVERY = "heat recovery system for mixer showers"
    OIL_CONDENSING_BOILER = "condensing oil boiler with radiators"
    PARTY_WALL_INSULATION = "party wall insulation"
    REPLACE_BOILER_WITH_NEW_CONDENSING_BOILER = (
        "replace boiler with new condensing boiler"
    )
    REPLACE_HEATING_UNIT_WITH_CONDENSING_UNIT = (
        "replace heating unit with condensing unit"
    )
    REPLACEMENT_GLAZING_UNITS = "replacement glazing units"
    REPLACEMENT_WARM_AIR_UNIT = "replacement warm air unit"
    ROOM_HEATERS_TO_CONDENSING_BOILER = "change room heaters to condensing boiler"
    ROOM_IN_ROOF_INSULATION = "room-in-roof insulation"
    SECONDARY_GLAZING = "secondary glazing to single glazed windows"
    SOLAR_PV_25 = "solar photovoltaic panels, 2.5 kWp"
    SOLAR_WATER_HEATING = "Solar water heating"
    TIME_AND_TEMPERATURE_ZONE_CONTROL = "time and temperature zone control"
    UPGRADE_HEATING_CONTROLS = "upgrade heating controls"
    WIND_TURBINE = "wind turbine"
    WOOD_PELLET_STOVE_WITH_BOILER_AND_RADIATORS = (
        "wood pellet stove with boiler and radiators"
    )


class AssessmentType(StrEnum):
    SAP_NEW_DWELLING = "SAP, new dwelling"
    SAP_EXISTING_DWELLING = "SAP, existing dwelling"
    RDSAP_EXISTING_DWELLING = "RdSAP, existing dwelling"


class EfficiencyRating(StrEnum):
    NA = "not applicable"
    VERY_POOR = "very poor"
    POOR = "poor"
    AVERAGE = "average"
    GOOD = "good"
    VERY_GOOD = "very good"


class WallType(StrEnum):
    CAVITY_WALL = "cavity wall"
    COB = "cob"
    GRANITE_OR_WHINSTONE = "granite or whinstone"
    PARK_HOME_WALL = "park home wall"
    SANDSTONE_OR_LIMESTONE = "sandstone or limestone"
    SOLID_BRICK = "solid brick"
    SYSTEM_BUILT = "system built"
    TIMBER_FRAME = "timber frame"

    @property
    def is_solid(self) -> bool:
        return self in {
            self.SOLID_BRICK,
            self.SANDSTONE_OR_LIMESTONE,
            self.GRANITE_OR_WHINSTONE,
        }


class WallInsulationType(StrEnum):
    EXTERNAL_INSULATION = "external insulation"
    FILLED_CAVITY = "filled cavity"
    FILLED_CAVITY_AND_EXTERNAL_INSULATION = "filled cavity and external insulation"
    FILLED_CAVITY_AND_INTERNAL_INSULATION = "filled cavity and internal insulation"
    INSULATED = "insulated"
    INTERNAL_INSULATION = "internal insulation"
    NO_INSULATION = "no insulation"
    PARTIAL_INSULATION = "partial insulation"


class WindowGlazingType(StrEnum):
    DOUBLE_GLAZING = "double glazing"
    FULLY_DOUBLE_GLAZED = "fully double glazed"
    FULL_SECONDARY_GLAZING = "full secondary glazing"
    FULLY_TRIPLE_GLAZED = "fully triple glazed"
    HIGH_PERFORMANCE_GLAZING = "high performance glazing"
    MOSTLY_DOUBLE_GLAZING = "mostly double glazing"
    MOSTLY_MULTIPLE_GLAZING = "mostly multiple glazing"
    MOSTLY_SECONDARY_GLAZING = "mostly secondary glazing"
    MOSTLY_TRIPLE_GLAZING = "mostly triple glazing"
    MULTIPLE_GLAZING_THROUGHOUT = "multiple glazing throughout"
    PARTIAL_DOUBLE_GLAZING = "partial double glazing"
    PARTIAL_MULTIPLE_GLAZING = "partial multiple glazing"
    PARTIAL_SECONDARY_GLAZING = "partial secondary glazing"
    PARTIAL_TRIPLE_GLAZING = "partial triple glazing"
    SINGLE_GLAZED = "single glazed"
    SINGLE_GLAZED_DOUBLE_GLAZING = "single glazed double glazing"
    SINGLE_GLAZED_SECONDARY_GLAZING = "single glazed secondary glazing"
    SOME_DOUBLE_GLAZING = "some double glazing"
    SOME_MULTIPLE_GLAZING = "some multiple glazing"
    SOME_SECONDARY_GLAZING = "some secondary glazing"
    SOME_TRIPLE_GLAZING = "some triple glazing"
    UNKNOWN_COMPLEX_GLAZING_REGIME = "unknown complex glazing regime"


class FlatLevel(StrEnum):
    BASEMENT = "basement"
    GROUND_FLOOR = "ground floor"
    MID_FLOOR = "mid floor"
    TOP_FLOOR = "top floor"


class HeatLossCorridor(StrEnum):
    HEATED_CORRIDOR = "heated corridor"
    NO_CORRIDOR = "no corridor"
    UNHEATED_CORRIDOR = "unheated corridor"


class MechanicalVentilation(StrEnum):
    MECHANICAL_SUPPLY_AND_EXTRACT = "mechanical, supply and extract"
    MECHANICAL_EXTRACT_ONLY = "mechanical, extract only"
    NATURAL = "natural"


class MeterType(StrEnum):
    DUAL_RATE = "dual"
    DUAL_RATE_24_HOUR = "dual (24 hour)"
    OFF_PEAK_18_HOUR = "off-peak 18 hour"
    SINGLE_RATE = "Single"


class MultipleGlazingType(StrEnum):
    DOUBLE_GLAZING_INSTALLED_DURING_OR_AFTER_2002 = (
        "double glazing installed during or after 2002"
    )
    DOUBLE_GLAZING_INSTALLED_BEFORE_2002 = "double glazing installed before 2002"
    DOUBLE_GLAZING_KNOWN_DATA = "double, known data"
    DOUBLE_GLAZING_UNKNOWN_INSTALL_DATE = "double glazing, unknown install date"
    SECONDARY_GLAZING = "secondary glazing"
    SINGLE_GLAZING = "single glazing"
    TRIPLE_GLAZING = "triple glazing"
    TRIPLE_GLAZING_KNOWN_DATA = "triple, known data"


class Tenure(StrEnum):
    OWNER_OCCUPIED = "owner-occupied"
    RENTED_PRIVATE = "rented (private)"
    RENTED_SOCIAL = "rented (social)"


class TransactionType(StrEnum):
    ASSESSMENT_FOR_GREEN_DEAL = "assessment for green deal"
    ECO_ASSESSMENT = "ECO assessment"
    FIT_APPLICATION = "FiT application"
    FOLLOWING_GREEN_DEAL = "following green deal"
    MARKETED_SALE = "marketed sale"
    NEW_DWELLING = "new dwelling"
    NON_MARKETED_SALE = "non marketed sale"
    OTHER = "other"
    RENTAL = "rental"
    RENTAL_PRIVATE = "rental (private)"
    RENTAL_SOCIAL = "rental (social)"
    RHI_APPLICATION = "RHI application"


class BuiltForm(StrEnum):
    DETACHED = "detached"
    ENCLOSED_END_TERRACE = "enclosed End-Terrace"
    ENCLOSED_MID_TERRACE = "enclosed Mid-Terrace"
    END_TERRACE = "end-Terrace"
    MID_TERRACE = "mid-Terrace"
    SEMI_DETACHED = "semi-Detached"


class PropertyType(StrEnum):
    BUNGALOW = "bungalow"
    FLAT = "flat"
    HOUSE = "house"
    MAISONETTE = "maisonette"
    PARK_HOME = "park home"


class RoofType(StrEnum):
    FLAT = "flat"
    PITCHED = "pitched"
    ROOF_ROOM = "roof room(s)"
    THATCHED = "thatched"
    DWELLING_ABOVE = "another dwelling/premises above"


class FloorType(StrEnum):
    CONSERVATORY = "conservatory"
    SOLID = "solid"
    SUSPENDED = "suspended"
    TO_EXTERNAL_AIR = "to external air"
    TO_UNHEATED_SPACE = "to unheated space"
    DWELLING_BELOW = "another dwelling/premises below"


class Orientation(StrEnum):
    NORTH = "north"
    NORTH_EAST = "north east"
    EAST = "east"
    SOUTH_EAST = "south east"
    SOUTH = "south"
    SOUTH_WEST = "south west"
    WEST = "west"
    NORTH_WEST = "north west"

    @property
    def angle(self) -> int:
        """
        Gets the angle of orientation relative to north (0).
        """
        return {
            Orientation.NORTH: 0,
            Orientation.NORTH_EAST: 45,
            Orientation.EAST: 90,
            Orientation.SOUTH_EAST: 135,
            Orientation.SOUTH: 180,
            Orientation.SOUTH_WEST: 225,
            Orientation.WEST: 270,
            Orientation.NORTH_WEST: 315,
        }[self]


class Overshading(StrEnum):
    NONE_OR_VERY_LITTLE = "none or very little"
    MODEST = "modest"
    SIGNIFICANT = "significant"
    HEAVY = "heavy"


class HotWaterSystemType(StrEnum):
    BACK_BOILER_GAS = "back boiler (gas)"
    COMMUNITY_HEAT_PUMP = "community heat pump"
    COMMUNITY_SCHEME = "community scheme"
    CIRCULATOR_GAS_WARM_AIR = (
        "from a circulator built into a gas warm air system, 1998 or later"
    )
    ELECTRIC_HEAT_PUMP = "electric heat pump"
    ELECTRIC_IMMERSION = "electric immersion"
    ELECTRIC_INSTANTANEOUS_AT_POINT_OF_USE = "electric instantaneous at point of use"
    FROM_MAIN_SYSTEM = "from main system"
    FROM_SECONDARY_SYSTEM = "from secondary system"
    GAS_BOILER_CIRCULATOR = "gas boiler/circulator"
    GAS_INSTANTANEOUS_AT_POINT_OF_USE = "gas instantaneous at point of use"
    GAS_RANGE_COOKER = "gas range cooker"
    HEAT_PUMP = "heat pump"
    OIL_BOILER_CIRCULATOR = "oil boiler/circulator"
    OIL_RANGE_COOKER = "oil range cooker"
    SOLID_FUEL_BOILER_CIRCULATOR = "solid fuel boiler/circulator"
    SOLID_FUEL_RANGE_COOKER = "solid fuel range cooker"
    GAS_MULTIPOINT = "gas multipoint"


class Tariff(StrEnum):
    STANDARD = "standard"
    OFF_PEAK = "off-peak"


class HeatingSystemSource(StrEnum):
    AIR_SOURCE_HEAT_PUMP = "air source heat pump"
    BOILER = "boiler"
    CEILING_HEATING = "ceiling heating"
    COMMUNITY_SCHEME = "community scheme"
    EXHAUST_AIR_MEV_SOURCE_HEAT_PUMP = "exhaust air MEV source heat pump"
    GROUND_SOURCE_HEAT_PUMP = "ground source heat pump"
    MICRO_COGENERATION = "micro-cogeneration"
    PORTABLE_HEATERS = "portable heaters"
    ELECTRIC_UNDERFLOOR_HEATERS = "electric underfloor heating"
    ROOM_HEATERS = "room heaters"
    STORAGE_HEATERS = "storage heaters"
    UNKNOWN_HEAT_PUMP = "unkown heat pump"
    WATER_SOURCE_HEAT_PUMP = "water source heat pump"
    COMMUNITY_SCHEME_RECOVERED_HEAT_FROM_BOILERS = (
        "community scheme recovered heat from boilers"
    )


class HeatingSystemCategory(StrEnum):
    BOILER_WITH_RADIATORS_OR_UNDERFLOOR_HEATING = (
        "boiler with radiators or underfloor heating"
    )
    COMMUNITY_HEATING_SYSTEM = "community heating system"
    ELECTRIC_UNDERFLOOR_HEATING = "electric underfloor heating"
    WARM_AIR_SYSTEM_NOT_HEAT_PUMP = "warm air system (not heat pump)"
    HEAT_PUMP_WITH_RADIATORS_OR_UNDERFLOOR_HEATING = (
        "heat pump with radiators or underfloor heating"
    )
    MICRO_COGENERATION = "micro-cogeneration"
    NOT_RECORDED = "not recorded"
    ROOM_HEATERS = "room heaters"
    NONE = "none"  # The literal string None encoded in the data.
    HEAT_PUMP_WITH_WARM_AIR_DISTRIBUTION = "heat pump with warm air distribution"
    ELECTRIC_STORAGE_HEATERS = "electric storage heaters"
    OTHER_SYSTEM = "other system"


class HeatingSystemEmitter(StrEnum):
    RADIATORS = "radiators"
    UNDERFLOOR = "underfloor"
    WARM_AIR = "warm air"


class HeatingControlMethod(StrEnum):
    TRV = "trv"
    BYPASS = "bypass"
    NONE = "none"
    BOILER_ENERGY_MANAGER = "boiler energy manager"
    MULTIROOM_THERMOSTAT = "two or more room thermostats"
    CHARGING_SYSTEM_LINKED_TO_USE_OF_COMMUNITY_HEATING = (
        "charging system linked to use of community heating"
    )
    APPLIANCE_THERMOSTATS = "appliance thermostats"
    UNIT_CHARGING = "unit charging"
    SINGLEROOM_THERMOSTAT = "single room thermostat"
    PROGRAMMER = "programmer"
    TIME_AND_TEMPERATURE_ZONE_CONTROL = "time and temperature zone control"
    FLOW_SWITCH = "flow switch"
    CELECT_CONTROLS = "celect controls"
    CONTROLS_FOR_HIGH_HEAT_RETENTION_STORAGE_HEATERS = (
        "controls for high heat retention storage heaters"
    )
    MANUAL_CHARGE_CONTROL = "manual charge control"
    FLAT_RATE_CHARGING = "flat rate charging"
    AUTOMATIC_CHARGE_CONTROL = "auto charge control"


class HeatingSystemEnergySource(StrEnum):
    B30D = "B30D"
    B30K = "B30K"
    BIOETHANOL = "bioethanol"
    BIODIESEL = "biodiesel"
    BIOGAS = "biogas"
    BIOMASS = "biomass"
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
    WASTE_COMBUSTION = "waste combustion"
    WOOD_CHIPS = "wood chips"
    WOOD_LOGS = "wood logs"
    WOOD_PELLETS = "wood pellets"


class AgeBand(StrEnum):
    """
    EPC age bands.
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"  # noqa: E741
    J = "J"
    K = "K"
    L = "L"
    M = "M"

    @classmethod
    def _band_authority_years(
        cls,
    ) -> dict["AgeBand", dict[EPCCountry | T_ParkHome, YearRange | None]]:
        return {
            cls.A: {
                EPCCountry.ENGLAND_AND_WALES: (None, 1899),
                EPCCountry.SCOTLAND: (None, 1918),
                EPCCountry.NORTHERN_IRELAND: (None, 1918),
                PARK_HOME: None,
            },
            cls.B: {
                EPCCountry.ENGLAND_AND_WALES: (1900, 1929),
                EPCCountry.SCOTLAND: (1919, 1929),
                EPCCountry.NORTHERN_IRELAND: (1919, 1929),
                PARK_HOME: None,
            },
            cls.C: {
                EPCCountry.ENGLAND_AND_WALES: (1930, 1949),
                EPCCountry.SCOTLAND: (1930, 1949),
                EPCCountry.NORTHERN_IRELAND: (1930, 1949),
                PARK_HOME: None,
            },
            cls.D: {
                EPCCountry.ENGLAND_AND_WALES: (1950, 1966),
                EPCCountry.SCOTLAND: (1950, 1964),
                EPCCountry.NORTHERN_IRELAND: (1950, 1973),
                PARK_HOME: None,
            },
            cls.E: {
                EPCCountry.ENGLAND_AND_WALES: (1967, 1975),
                EPCCountry.SCOTLAND: (1965, 1975),
                EPCCountry.NORTHERN_IRELAND: (1974, 1977),
                PARK_HOME: None,
            },
            cls.F: {
                EPCCountry.ENGLAND_AND_WALES: (1976, 1982),
                EPCCountry.SCOTLAND: (1976, 1983),
                EPCCountry.NORTHERN_IRELAND: (1978, 1985),
                PARK_HOME: (None, 1982),
            },
            cls.G: {
                EPCCountry.ENGLAND_AND_WALES: (1983, 1990),
                EPCCountry.SCOTLAND: (1984, 1991),
                EPCCountry.NORTHERN_IRELAND: (1986, 1991),
                PARK_HOME: (1983, 1995),
            },
            cls.H: {
                EPCCountry.ENGLAND_AND_WALES: (1991, 1995),
                EPCCountry.SCOTLAND: (1992, 1998),
                EPCCountry.NORTHERN_IRELAND: (1992, 1999),
                PARK_HOME: None,
            },
            cls.I: {
                EPCCountry.ENGLAND_AND_WALES: (1996, 2002),
                EPCCountry.SCOTLAND: (1999, 2002),
                EPCCountry.NORTHERN_IRELAND: (2000, 2006),
                PARK_HOME: (1996, 2005),
            },
            cls.J: {
                EPCCountry.ENGLAND_AND_WALES: (2003, 2006),
                EPCCountry.SCOTLAND: (2003, 2007),
                EPCCountry.NORTHERN_IRELAND: None,
                PARK_HOME: None,
            },
            cls.K: {
                EPCCountry.ENGLAND_AND_WALES: (2007, 2011),
                EPCCountry.SCOTLAND: (2008, 2011),
                EPCCountry.NORTHERN_IRELAND: (2007, 2013),
                PARK_HOME: (2006, None),
            },
            cls.L: {
                EPCCountry.ENGLAND_AND_WALES: (2012, 2022),
                EPCCountry.SCOTLAND: (2012, 2023),
                EPCCountry.NORTHERN_IRELAND: (
                    2014,
                    2022,
                ),  # "2014 onwards" on RdSAP10 so in conflict with M
                PARK_HOME: None,
            },
            cls.M: {
                EPCCountry.ENGLAND_AND_WALES: (2023, None),
                EPCCountry.SCOTLAND: (2024, None),
                EPCCountry.NORTHERN_IRELAND: (2023, None),  # "2023 onwards" on RdSAP10
                PARK_HOME: None,
            },
        }

    def years(self, authority: EPCCountry | T_ParkHome) -> YearRange | None:
        return self._band_authority_years()[self][authority]

    def year_in_band(self, year: int, authority: EPCCountry | T_ParkHome) -> bool:
        years = self.years(authority)
        if years is None or isinstance(years, EmptyRange):
            return False
        band_from = years[0]
        band_to = years[1]
        return (band_from is None or band_from <= year) and (
            band_to is None or band_to >= year
        )

    @classmethod
    def from_year(cls, year: int, authority: EPCCountry | T_ParkHome) -> "AgeBand":
        for band in AgeBand:
            if band.year_in_band(year, authority):
                return band
        raise ValueError(  # pragma: no cover  # only possible if there's an error in _band_authority_years()
            f"Age band not found for year {year} and authority {authority}"
        )

    @classmethod
    def from_year_range(
        cls, year_range: YearRange, authority: EPCCountry | T_ParkHome
    ) -> "AgeBand":
        if isinstance(year_range, EmptyRange):
            raise ValueError("from_year_range() called for EmptyRange")
        lower = year_range[0]
        upper = year_range[1]
        if lower is None and upper is None:
            raise ValueError("from_year_range() called for YearRange(None, None)")
        if lower is not None:
            return cls.from_year(lower, authority)
        # if there is no lower bound, then we think the house was built BEFORE the upper bound.
        # so the build year is in the year  before that.
        return cls.from_year(upper - 1, authority)  # type:ignore


class _ABCIntEnumMeta(ABCMeta, EnumMeta):
    pass


class EPCIntEnum(ABC, IntEnum, metaclass=_ABCIntEnumMeta):
    @abstractmethod
    def to_str_enum(self) -> StrEnum | None:
        pass

    @classmethod
    def from_rdsap_xml(cls, value: str):
        if value == "ND":
            return None
        return cls(int(value)).to_str_enum()


class MeterTypeInt(EPCIntEnum):
    DUAL_RATE = 1
    DUAL_RATE_24_HOUR = 4
    OFF_PEAK_18_HOUR = 5
    SINGLE_RATE = 2

    def to_str_enum(self) -> MeterType | None:
        return getattr(MeterType, self.name, None)


class PropertyTypeInt(EPCIntEnum):
    HOUSE = 0
    BUNGALOW = 1
    FLAT = 2
    MAISONETTE = 3
    PARK_HOME = 4

    def to_str_enum(self) -> PropertyType:
        return PropertyType[self.name]


class BuiltFormInt(EPCIntEnum):
    DETACHED = 1
    SEMI_DETACHED = 2
    END_TERRACE = 3
    MID_TERRACE = 4
    ENCLOSED_END_TERRACE = 5
    ENCLOSED_MID_TERRACE = 6

    def to_str_enum(self) -> BuiltForm:
        return BuiltForm[self.name]


class GlazedArea(StrEnum):
    # Ordered in case we ever care about comparison operators...
    LESS_THAN_TYPICAL = "Less than typical"
    MUCH_LESS_THAN_TYPICAL = "Much less than typical"
    TYPICAL = "Typical"
    MORE_THAN_TYPICAL = "More than typical"
    MUCH_MORE_THAN_TYPICAL = "Much more than typical"


class GlazedAreaInt(EPCIntEnum):
    TYPICAL = 1
    MORE_THAN_TYPICAL = 2
    LESS_THAN_TYPICAL = 3
    MUCH_MORE_THAN_TYPICAL = 4
    MUCH_LESS_THAN_TYPICAL = 5

    def to_str_enum(self) -> GlazedArea:
        return GlazedArea[self.name]


class EfficiencyRatingInt(EPCIntEnum):
    NA = 0
    VERY_POOR = 1
    POOR = 2
    AVERAGE = 3
    GOOD = 4
    VERY_GOOD = 5

    def to_str_enum(self) -> EfficiencyRating | None:
        return EfficiencyRating[self.name]


class MultipleGlazingTypeInt(EPCIntEnum):
    DOUBLE_GLAZING_INSTALLED_BEFORE_2002 = 1
    DOUBLE_GLAZING_INSTALLED_DURING_OR_AFTER_2002 = 2
    DOUBLE_GLAZING_UNKNOWN_INSTALL_DATE = 3
    SECONDARY_GLAZING = 4
    SINGLE_GLAZING = 5
    TRIPLE_GLAZING = 6
    DOUBLE_GLAZING_KNOWN_DATA = 7
    TRIPLE_GLAZING_KNOWN_DATA = 8

    def to_str_enum(self) -> MultipleGlazingType | None:
        return MultipleGlazingType[self.name]


class FlatLevelInt(EPCIntEnum):
    BASEMENT = 0
    GROUND_FLOOR = 1
    MID_FLOOR = 2
    TOP_FLOOR = 3

    def to_str_enum(self) -> FlatLevel | None:
        return FlatLevel[self.name]

    @classmethod
    def from_rdsap_xml(cls, value: str):
        if value == "99":
            return None
        return super().from_rdsap_xml(value)


class HeatLossCorridorInt(EPCIntEnum):
    NO_CORRIDOR = 0
    HEATED_CORRIDOR = 1
    UNHEATED_CORRIDOR = 2

    def to_str_enum(self) -> HeatLossCorridor | None:
        return HeatLossCorridor[self.name]


class ImprovementTypeInt(EPCIntEnum):
    # TODO these ImprovementType values dont map to rdsap enums
    # CONDENSING_BOILER = "condensing boiler"
    # UPGRADE_HEATING_CONTROLS = "upgrade heating controls"
    INSULATE_HOT_WATER_CYLINDER_WITH_80_MM_JACKET = 1
    INCREASE_HOT_WATER_CYLINDER_INSULATION = 2
    ADDITIONAL_80_MM_JACKET_TO_HOT_WATER_CYLINDER = 3
    HOT_WATER_CYLINDER_THERMOSTAT = 4
    INCREASE_LOFT_INSULATION_TO_270_MM = 5
    CAVITY_WALL_INSULATION = 6
    INTERNAL_OR_EXTERNAL_WALL_INSULATION = 7
    DOUBLE_GLAZING = 8
    SECONDARY_GLAZING = 9
    DRAUGHTPROOFING = 10
    HEATING_CONTROLS_PROGRAMMER_ROOM_THERMOSTAT_AND_TRVS = 11  # does not map
    HEATING_CONTROLS_ROOM_THERMOSTAT_AND_TRVS = 12  # does not map
    HEATING_CONTROLS_THERMOSTATIC_RADIATOR_VALVES = 13  # does not map
    HEATING_CONTROLS_ROOM_THERMOSTAT = 14  # does not map
    HEATING_CONTROLS_PROGRAMMER_AND_TRVS = 15  # does not map
    TIME_AND_TEMPERATURE_ZONE_CONTROL = 16
    HEATING_CONTROLS_PROGRAMMER_AND_ROOM_THERMOSTAT = 17  # does not map
    HEATING_CONTROLS_ROOM_THERMOSTAT1 = 18  # does not map
    SOLAR_WATER_HEATING = 19
    REPLACE_BOILER_WITH_NEW_CONDENSING_BOILER = 20
    REPLACE_BOILER_WITH_NEW_CONDENSING_BOILER1 = 21
    BIOMASS_BOILER = 22
    WOOD_PELLET_STOVE_WITH_BOILER_AND_RADIATORS = 23
    FAN_ASSISTED_STORAGE_HEATERS_AND_DUAL_IMMERSION_CYLINDER = 24
    FAN_ASSISTED_STORAGE_HEATERS = 25
    REPLACEMENT_WARM_AIR_UNIT = 26
    GAS_CONDENSING_BOILER = 27
    OIL_CONDENSING_BOILER = 28
    CHANGE_HEATING_TO_GAS_CONDENSING_BOILER1 = 29
    FAN_ASSISTED_STORAGE_HEATERS_AND_DUAL_IMMERSION_CYLINDER1 = 30
    FANASSISTED_STORAGE_HEATERS = 31
    CHANGE_HEATING_TO_GAS_CONDENSING_BOILER12 = 32
    SOLAR_PV_25 = 34
    LOW_ENERGY_LIGHTING = 35
    REPLACE_HEATING_UNIT_WITH_CONDENSING_UNIT = 36
    CONDENSING_BOILER_SEPARATE_FROM_THE_RANGE_COOKER = 37
    CONDENSING_BOILER_SEPARATE_FROM_THE_RANGE_COOKER1 = 38
    WOOD_PELLET_STOVE_WITH_BOILER_AND_RADIATORS1 = 39
    ROOM_HEATERS_TO_CONDENSING_BOILER = 40
    CHANGE_ROOM_HEATERS_TO_CONDENSING_BOILER1 = 41
    REPLACE_HEATING_UNIT_WITH_MAINS_GAS_CONDENSING_UNIT = 42
    CONDENSING_OIL_BOILER_WITH_RADIATORS1 = 43
    WIND_TURBINE = 44
    FLAT_ROOF_INSULATION = 45
    ROOM_IN_ROOF_INSULATION = 46
    FLOOR_INSULATION = 47
    HIGH_PERFORMANCE_EXTERNAL_DOORS = 48
    MIXER_SHOWER_HEAT_RECOVERY = 49
    BOILER_FLUE_GAS_HEAT_RECOVERY = 50
    AIR_OR_GROUND_SOURCE_HEAT_PUMP = 51  # does not map
    AIR_OR_GROUND_SOURCE_HEAT_PUMP_WITH_UNDERFLOOR_HEATING = 52  # does not map
    MICRO_CHP = 53  # does not map
    BIOMASS_BOILER_EXEMPTED_APPLIANCE_IF_IN_SMOKE_CONTROL_AREA = 54  # does not map
    EXTERNAL_INSULATION_WITH_CAVITY_WALL_INSULATION = 55  # does not map
    REPLACEMENT_GLAZING_UNITS = 56
    FLOOR_INSULATION_SUSPENDED_FLOOR = 57
    FLOOR_INSULATION_SOLID_FLOOR = 58
    HIGH_HEAT_RETENTION_STORAGE_HEATERS_AND_DUAL_IMMERSION_CYLINDER = 59
    HIGH_HEAT_RETENTION_STORAGE_HEATERS = 60
    HIGH_HEAT_RETENTION_STORAGE_HEATERS_AND_DUAL_IMMERSION_CYLINDER1 = 61
    HIGH_HEAT_RETENTION_STORAGE_HEATERS1 = 62
    PARTY_WALL_INSULATION = 63  # does not map

    def to_str_enum(self) -> ImprovementType | None:
        # not all names map cleanly. Try self.name first,
        # followed by self.name without trailing numbers
        return getattr(
            ImprovementType,
            self.name,
            getattr(ImprovementType, re.sub(r"[0-9]+$", "", self.name), None),
        )


class OrientationInt(EPCIntEnum):
    NORTH = 1
    NORTH_EAST = 2
    EAST = 3
    SOUTH_EAST = 4
    SOUTH = 5
    SOUTH_WEST = 6
    WEST = 7
    NORTH_WEST = 8

    def to_str_enum(self) -> Orientation | None:
        return Orientation[self.name]


class OvershadingCodeInt(EPCIntEnum):
    NONE_OR_VERY_LITTLE = 1
    MODEST = 2
    SIGNIFICANT = 3
    HEAVY = 4

    def to_str_enum(self) -> Overshading | None:
        return Overshading[self.name]


class EPCRating(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

    # SAP 10.2 Table 13: Rating bands
    __SCORE_RANGES: Final[dict[str, range]] = {
        "A": range(92, 101),  # Technically allows >100 scores, but we cap to 100.
        "B": range(81, 92),
        "C": range(69, 81),
        "D": range(55, 69),
        "E": range(39, 55),
        "F": range(21, 39),
        "G": range(0, 21),
    }

    @classmethod
    @functools.cache
    def from_score(cls, score: int) -> "EPCRating":
        for key, score_range in cls.__SCORE_RANGES.items():
            if score in score_range:
                return cls(key)
        raise ValueError(f"Unhandled SAP score value: {score}")

    @functools.cached_property
    def score_range(self) -> range:
        return EPCRating.__SCORE_RANGES[self.value]
