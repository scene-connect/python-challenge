from decimal import Decimal
from typing import Literal

import pydantic
import typing_extensions
from geojson_pydantic import Point

from . import enums
from . import epc_enums
from . import simulation_enums
from .basic import MonthNumber
from .basic import YearRange
from .enums import DomesticEnergyEndUse
from .enums import EnergySource
from .pydantic.fields import UPRN
from .pydantic.fields import FloatJSONRound
from .simulation import HeatingControlMethod
from .simulation import HeatingSystem
from .simulation import HotWaterSystem
from .simulation import SolarPVArray
from .simulation_enums import HotWaterSource


class EnergyConsumptionSummary(pydantic.BaseModel):
    energy: FloatJSONRound = pydantic.Field(title="Energy (kWh)")
    co2e: FloatJSONRound = pydantic.Field(
        title="Carbon and equivalent emissions (KG/co2e)"
    )
    operating_cost: FloatJSONRound = pydantic.Field(
        title="Operating cost (£)",
        description="The operating cost of this energy usage.",
    )


class EnergyGenerationSummary(pydantic.BaseModel):
    energy_generated: FloatJSONRound = pydantic.Field(
        title="Energy generated (kWh)",
    )
    energy_self_consumed: FloatJSONRound = pydantic.Field(
        title="Energy self-consumed by the customer (kWh)",
    )
    energy_exported: FloatJSONRound = pydantic.Field(
        title="Energy exported (kWh)",
    )
    co2e_reduction: FloatJSONRound = pydantic.Field(
        title="""
        Carbon and equivalent emissions reduction (KG CO2e) relative to the grid
        intensity of the energy generated (both self-consumed and exported).
        """,
    )
    operating_cost_reduction_total: FloatJSONRound = pydantic.Field(
        title="Operating cost reduction (£)",
        description="""
        The reduction in operating costs from using the generated energy.
        This covers both savings from self-consumption and revenue from export.
        """,
    )
    export_revenue: FloatJSONRound = pydantic.Field(title="Export revenue (£)")
    operating_cost_reduction_self_consumption: FloatJSONRound = pydantic.Field(
        title="Reduction in operating costs from self-consumption of generated energy."
    )


class EnergyProfile(pydantic.BaseModel):
    annual_energy_total: EnergyConsumptionSummary = pydantic.Field(
        description="""
        Annual total energy consumption, with cost and carbon (all energy sources).
        """,
    )

    annual_energy_sources: dict[EnergySource, EnergyConsumptionSummary] = (
        pydantic.Field(
            description="""
        Annual consumption of energy, cost and carbon by energy source.

        Keyed by ZUoS enum: EnergySource.

        Note: These figures concern energy consumption, and do not distinguish between
        grid electricity and self-generated electricity. For that data, see the
        'annual_energy_generation' field which reports on self-consumption and export
        of generated electricity.
        """,
        )
    )

    annual_energy_end_use: dict[DomesticEnergyEndUse, EnergyConsumptionSummary] = (
        pydantic.Field(
            description="""
        Annual energy consumption, by ECUK domestic energy end use category.

        Keyed by ZUoS enum: DomesticEnergyEndUse.
        """,
        )
    )

    annual_energy_generation: EnergyGenerationSummary = pydantic.Field(
        description="Annual self-generation of electricity.",
        # TODO probably a future note about batteries and their impact on total consumption
        # and self-consumption and total consumption, but that's for another time...
        # We may even decide to represent the battery entirely on as they're so different.
    )

    monthly_energy_total: dict[MonthNumber, EnergyConsumptionSummary] = pydantic.Field(
        description="""
        Monthly total energy consumption, keyed by month number (January=1) with cost
        and carbon (from all energy sources).
        """,
    )

    monthly_energy_sources: dict[
        MonthNumber, dict[EnergySource, EnergyConsumptionSummary]
    ] = pydantic.Field(
        description="""
        Monthly consumption of energy, keyed by month number (January=1) cost and carbon
        by energy source.
        """,
    )

    monthly_energy_end_use: dict[
        MonthNumber, dict[DomesticEnergyEndUse, EnergyConsumptionSummary]
    ] = pydantic.Field(
        description="""
        Monthly energy consumption, keyed by month number (January=1) by end use.
        """,
    )

    monthly_energy_generation: dict[MonthNumber, EnergyGenerationSummary] = (
        pydantic.Field(
            description="Monthly self-generation of electricity, keyed by month number (January=1).",
        )
    )

    peak_daily_energy_sources: dict[EnergySource, Decimal] = pydantic.Field(
        description="""
        The highest daily energy consumption, by energy source.

        Keyed by ZUoS enum: EnergySource.
        """
    )

    peak_daily_energy_end_use: dict[DomesticEnergyEndUse, Decimal] = pydantic.Field(
        description="""
        The highest daily energy consumption, by ECUK domestic energy end use category.

        Keyed by ZUoS enum: DomesticEnergyEndUse.
        """
    )

    peak_hourly_energy_sources: dict[EnergySource, Decimal] = pydantic.Field(
        description="""
        The highest hourly energy consumption, by energy source.

        Keyed by ZUoS enum: EnergySource.
        """
    )

    peak_hourly_energy_end_use: dict[DomesticEnergyEndUse, Decimal] = pydantic.Field(
        description="""
        The highest hourly energy consumption, by ECUK domestic energy end use category.

        Keyed by ZUoS enum: DomesticEnergyEndUse.
        """
    )

    predicted_epc_rating: epc_enums.EPCRating | None = pydantic.Field(
        description="Predicted EPC rating band of the simulated home.",
        default=None,
    )
    predicted_epc_score: int | None = pydantic.Field(
        description="Predicted EPC score of the simulated home.",
        default=None,
    )


class Door(pydantic.BaseModel):
    """
    Representation of external door.
    """

    average_thermal_transmittance: Decimal | None = pydantic.Field(
        description="U-value of the door", default=None
    )
    is_insulated: bool | None = None
    is_insulation_assumed: bool | None = pydantic.Field(
        description="Whether the insulation data is an assumption", default=None
    )
    direct_to_outside: bool | None = pydantic.Field(
        description="Whether or not this is a door directly to the outside (no corridor).",
        default=None,
    )


class Fabric(pydantic.BaseModel):
    is_as_built: bool | None = pydantic.Field(
        description="Whether the insulation is as built", default=None
    )
    has_insulation: bool | None = pydantic.Field(
        description="Whether the fabric element has insulation", default=None
    )
    is_insulation_assumed: bool | None = pydantic.Field(
        description="Whether the insulation data is an assumption", default=None
    )
    insulation_thickness: int | None = pydantic.Field(
        description="Insulation thickness (mm)", default=None
    )
    average_thermal_transmittance: Decimal | None = pydantic.Field(
        description="U-value of the fabric element", default=None
    )


class Wall(Fabric):
    """
    Representation of the wall fabric and insulation.

    Most of these correspond to the EPC fields.
    """

    wall_type: epc_enums.WallType | None = None
    wall_thickness: int | None = pydantic.Field(
        description="external wall thickness (mm)", default=None
    )
    surface_area: int | None = pydantic.Field(
        description="Surface area of the external walls (m2)", default=None, ge=0
    )
    perimeter: int | None = pydantic.Field(
        description="Perimeter of the external walls (m)", default=None, ge=0
    )
    insulation_position: epc_enums.WallInsulationType | None = pydantic.Field(
        description="Position of the wall insulation",
        default=None,
    )
    insulation_material: enums.InsulationMaterial | None = pydantic.Field(
        description="The material the wall was insulated with (if insulation is present at all)",
        default=None,
    )


class Floor(Fabric):
    floor_type: (
        Literal[
            epc_enums.FloorType.SOLID,
            epc_enums.FloorType.SUSPENDED,
            epc_enums.FloorType.CONSERVATORY,
        ]
        | None
    ) = None
    external_air_below: bool | None = None
    unheated_space_below: bool | None = None
    insulation_position: enums.FloorInsulationPosition | None = pydantic.Field(
        description="Position of the floor insulation", default=None
    )


class Roof(Fabric):
    roof_type: epc_enums.RoofType | None
    surface_area: float | None = pydantic.Field(
        description="The total surface area of the roof, including any windows if pitched (m2)",
        gt=0,
        default=None,
    )
    pitch: int | None = pydantic.Field(
        description="""
        Pitch of the roof, in degrees.
        Only present if the roof type is pitched.
        """,
        ge=0,
        le=90,
        default=None,
    )
    insulation_position: enums.RoofInsulationPosition | None = pydantic.Field(
        description="Position of the roof insulation", default=None
    )


class Glazing(pydantic.BaseModel):
    glazing_type: enums.WindowGlazingType | None = pydantic.Field(
        description="The type of window glazing, matching the EPC type", default=None
    )
    multiple_glazing_type: epc_enums.MultipleGlazingType | None = pydantic.Field(
        description="The type of multiple glazing, following the EPC definition",
        default=None,
    )
    multiple_glazing_percentage: int | None = pydantic.Field(
        description="The percentage of windows that is multiple-glazed",
        default=None,
        le=100,
        ge=0,
    )
    average_thermal_transmittance: Decimal | None = pydantic.Field(
        description="U-value of the glazing", default=None
    )
    installation_year_range: YearRange | None = pydantic.Field(
        description="""
        Year the windows were installed.
        """,
        default=None,
    )
    windows_construction: enums.WindowConstruction | None = None
    glazing_gap: enums.WindowGlazingGap | None = pydantic.Field(
        description="""
            The gap between window glazing panes.
            For triple glazing, this is the gap between each pane, not the total gap from
            interior to exterior.
            """,
        default=None,
    )
    sap_glazed_area: epc_enums.GlazedAreaInt | None = pydantic.Field(
        description="Ranged estimate of the total glazed area",
        ge=1,
        le=5,
        default=None,
    )
    glazing_ratio: float | None = pydantic.Field(
        description="SAP glazing to wall ratio.",
        ge=0,
        le=1,
        default=None,
    )


class UKAddress(pydantic.BaseModel):
    lines: list[str] = pydantic.Field(min_length=1, max_length=3)
    town: str = pydantic.Field(min_length=1)
    postcode: str = pydantic.Field(min_length=1)
    country: Literal["United Kingdom"] = "United Kingdom"

    @pydantic.field_validator("lines", mode="after")
    @classmethod
    def lines_not_empty(cls, value: list[str]) -> list[str]:
        if not value[0]:
            raise ValueError("First line of address must not be empty.")
        # Remove empty strings just for neatness.
        return [line for line in value if line]

    def __str__(self) -> str:
        return ", ".join(
            [
                part
                for part in self.lines + [self.town, self.postcode, self.country]
                if part
            ]
        )


class HomePartial(pydantic.BaseModel):
    """
    Partial Home object with optional fields.

    The partial is defined first, so that the full Home class is always compatible
    with its parent. If HomePartial was a child of Home, it would contain values (Nones)
    which could not be applied to the parent class. This way, a valid `Home` is always
    a valid HomePartial.
    """

    #
    # Optional fields on HomePartial which are required on Home.
    #
    location: Point | None = None
    property_type: epc_enums.PropertyType | None = None
    built_form: epc_enums.BuiltForm | None = None
    age_band: epc_enums.AgeBand | None = None
    north_angle: int | None = pydantic.Field(default=None, ge=0, lt=360)
    total_floor_area: int | None = pydantic.Field(gt=0, default=None)
    room_height: float | None = pydantic.Field(
        ge=2,
        lt=5,
        default=None,
    )
    levels: list[simulation_enums.Level] | None = None
    wall: Wall | None = None
    external_wall_count: int | None = pydantic.Field(gt=0, default=None)
    footprint: float | None = pydantic.Field(gt=0, default=None)
    glazing: Glazing | None = None
    window_count: int | None = None
    doors: list[Door] | None = None
    is_mains_gas_present: bool | None = None
    main_heating_systems: list[HeatingSystem] | None = pydantic.Field(
        min_length=1,
        default=None,
    )
    hot_water_systems: list[HotWaterSystem] | None = pydantic.Field(
        min_length=1,
        default=None,
    )
    fixed_lighting_outlets_count: int | None = pydantic.Field(default=None, ge=0)
    low_energy_lighting_outlets_count: int | None = pydantic.Field(
        default=None,
        ge=0,
    )
    low_energy_lighting_percentage: float | None = pydantic.Field(
        default=None,
        ge=0,
        le=100,
    )

    #
    # Always optional fields (only defined on HomePartial).
    #

    uprn: UPRN | None = pydantic.Field(
        description="""
        UPRN of the home.
        Used to look up the 'location' if not known.
        """,
        default=None,
    )
    address: UKAddress | None = pydantic.Field(
        description="""
        Address of the home.
        Used to look up the 'location' if that and 'uprn' are not known.
        """,
        default=None,
    )
    floor: Floor | None = pydantic.Field(
        default=None,
        description="Ground floor of the home, if present. Flats above ground-floor do not need to define a floor.",
    )
    roof: Roof | None = pydantic.Field(
        description="Roof of the home, if present. Mid-level flats do not need to define a roof.",
        default=None,
    )
    meter_type: epc_enums.MeterType | None = pydantic.Field(
        description="Type of electricity meter",
        default=None,
    )
    heat_loss_corridor: epc_enums.HeatLossCorridor | None = pydantic.Field(
        description="RdSAP property for flats/maisonettes, for whether there is a corridor/stairwell present.",
        default=None,
    )
    is_listed_building: bool | None = None
    is_in_conservation_area: bool | None = None
    habitable_room_count: int | None = pydantic.Field(
        description="Number of habitable rooms.",
        gt=0,
        default=None,
    )
    heated_room_count: int | None = pydantic.Field(
        description="Number of heated rooms.",
        gt=0,
        default=None,
    )
    draught_proofed_window_percentage: int | None = pydantic.Field(
        description="% of windows that has been draught proofed.",
        default=None,
        le=100,
        ge=0,
    )
    draught_proofed_door_percentage: int | None = pydantic.Field(
        description="% of doors that has been draught proofed.",
        default=None,
        le=100,
        ge=0,
    )
    secondary_heating_systems: list[HeatingSystem] | None = pydantic.Field(
        description="""
        Secondary heating system(s) of the Home.
        Must be at least one, if defined as a list.

        ZUoS does not currently simulate secondary heating systems for space heating,
        but the details may be used to model the hot water system if the source is set
        to "from secondary system".
        """,
        min_length=1,
        default=None,
    )
    heating_systems_controls: list[HeatingControlMethod] | None = pydantic.Field(
        description="Heating control methods of the main heating system(s)",
        default=None,
    )
    solar_pv: list[SolarPVArray] | None = pydantic.Field(
        description="""
        Solar PV array(s) on the home.
        Represent split-array systems which share one inverter as 2 arrays, with their
        unique azimuth/tilt, each with the full inverter_capacity.
        """,
        default=None,
    )
    available_pv_array_size: float | None = pydantic.Field(
        description="The total available area for PV arrays on the home.",
        default=None,
    )

    # Computed fields
    end_use_energy_sources: dict[DomesticEnergyEndUse, EnergySource] = pydantic.Field(
        description="Energy end-uses with their energy source.",
        default={},
    )

    # Optional fields direct from the EPC.
    # Not used directly for modelling the home energy use, but maybe used by other code
    # e.g. for predicting future EPC ratings.
    epc_suggested_improvements: set[epc_enums.ImprovementType] | None = None
    epc_rating: epc_enums.EPCRating | None = pydantic.Field(
        description="The EPC energy efficiency rating of the baseline Home, "
        "taken from the source EPC or RdSAP XML, if present.",
        default=None,
    )
    epc_score: int | None = pydantic.Field(
        description="The EPC energy efficiency score (0-100) of the baseline Home, "
        "taken from the source EPC or RdSAP XML, if present.",
        default=None,
    )

    def to_home(self) -> "Home":
        return Home(**self.model_dump())


class Home(HomePartial):
    """
    Full representation of a home to be simulated.
    """

    #
    # Required fields.
    #
    # Unfortunately, pyright is overly assertive that a child-class must have compatible
    # types with its parent, including optional in that restriction.
    # Similarly, they also have a check for missing default values for overridden fields.
    # So we have to have a lot of type ignores for reportGeneralTypeIssues.
    #

    location: Point = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="""
        Location of the home, as [latitude, longitude].
        If not known, can be looked up from either 'uprn' (preferred) or 'address'.
        """,
    )
    property_type: epc_enums.PropertyType  # type: ignore[reportGeneralTypeIssues]
    built_form: epc_enums.BuiltForm  # type: ignore[reportGeneralTypeIssues]
    age_band: epc_enums.AgeBand  # type: ignore[reportGeneralTypeIssues]
    north_angle: int = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="The angle from-north of the front door of the home.",
        ge=0,
        lt=360,
    )
    total_floor_area: int = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        gt=0,
        description="Total floor area (m2)",
    )
    room_height: float = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        ge=2,
        lt=5,
        description="""
            Interior room height, in metres.EPC field: floor_0_room_height.
            """,
    )
    levels: list[simulation_enums.Level] = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="""
            The building 'levels' (floors).
            Currently this is a simple list of level types.
            It may evolve into an ordered object of levels, with additional properties
            such as the construction properties of the floor (concrete, suspended timber, etc)
            """,
        min_length=1,
    )
    wall: Wall = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="External wall details",
    )
    external_wall_count: int = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="Number of external walls"
    )
    footprint: float = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        gt=0,
        description="Footprint of the home in m2.",
    )
    doors: list[Door] = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="Doors in external walls",
        min_length=1,
    )
    glazing: Glazing  # type: ignore[reportGeneralTypeIssues]
    window_count: int = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="Number of windows in external walls",
    )
    is_mains_gas_present: bool = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="""
            Whether there is a mains gas grid connection at the property.
            Null if unknown, ZUoS will attempt to assume based on the energy sources of the
            heating and hot water systems.
            """,
    )
    main_heating_systems: list[HeatingSystem] = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="""
        Main heating system(s) of the home.
        Must be at least one defined.
        ZUoS currently only simulates the first heating system in the list.
        """,
        min_length=1,
    )
    hot_water_systems: list[HotWaterSystem] = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="""
        Hot water system(s) of the home.
        Must be at least one defined.
        ZUoS currently only simulates the first hot water system in the list.
        """,
        min_length=1,
    )
    fixed_lighting_outlets_count: int = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="number of fixed lighting outlets",
        ge=0,
    )
    low_energy_lighting_outlets_count: int = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="number of fixed lighting outlets with low energy lighting",
        ge=0,
    )
    low_energy_lighting_percentage: float = pydantic.Field(  # type: ignore[reportGeneralTypeIssues]
        description="percentage of fixed lighting outlets with low energy lighting",
        ge=0,
        le=100,
    )

    @pydantic.field_validator("glazing", mode="after")
    def validate_glazing(cls, value: Glazing) -> Glazing:
        if value.glazing_ratio is None:
            raise ValueError(
                "glazing.glazing_ratio must be defined on a full Home object"
            )
        return value

    @pydantic.field_validator(
        "main_heating_systems", "secondary_heating_systems", mode="after"
    )
    def validate_heating_systems(
        cls, value: list[HeatingSystem] | None, info: pydantic.ValidationInfo
    ) -> list[HeatingSystem] | None:
        if value is None:
            # Secondary_heating_systems may be None, main pydantic validation ensures
            # that main_heating_systems type.
            return value
        for i, system in enumerate(value):
            trace = f"{info.field_name}[{i}]"
            if system.source is None:
                raise ValueError(
                    f"{trace}.source must be defined on a full Home object"
                )
            if system.energy_source is None:
                raise ValueError(
                    f"{trace}.energy_source must be defined on a full Home object"
                )
            if DomesticEnergyEndUse.SPACE_HEATING not in system.efficiency:
                raise ValueError(
                    f"{trace}.efficiency must contain {DomesticEnergyEndUse.SPACE_HEATING} on a full Home object"
                )
            if system.is_wet:
                if not system.emitters:
                    raise ValueError(
                        f"{trace}.emitters should be defined for a wet heating system"
                    )

        return value

    @pydantic.field_validator("hot_water_systems", mode="after")
    def validate_hot_water_systems(
        cls, value: list[HotWaterSystem]
    ) -> list[HotWaterSystem]:
        for i, system in enumerate(value):
            trace = f"hot_water_systems[{i}]"
            if system.source is None:
                raise ValueError(
                    f"{trace}.source must be defined on a full Home object"
                )
            if system.source not in [
                HotWaterSource.FROM_MAIN_SYSTEM,
                HotWaterSource.FROM_SECONDARY_SYSTEM,
            ]:
                if system.energy_source is None:
                    raise ValueError(
                        f"{trace}.energy_source must be defined on a full Home object, "
                        "unless source is from main/secondary system"
                    )
                if DomesticEnergyEndUse.HOT_WATER not in system.efficiency:
                    raise ValueError(
                        f"{trace}.efficiency must contain '{DomesticEnergyEndUse.HOT_WATER}' "
                        "on a full Home object, unless source is from main/secondary system"
                    )
        return value

    @pydantic.model_validator(mode="after")
    def validate_hot_water_systems_from_heating_system(self) -> typing_extensions.Self:
        for i, hot_water_system in enumerate(self.hot_water_systems):
            if DomesticEnergyEndUse.HOT_WATER in hot_water_system.efficiency:
                continue
            # Allow from-x-system to get efficiency from that system instead of defining
            # it itself.
            match hot_water_system.source:
                case HotWaterSource.FROM_MAIN_SYSTEM:
                    heating_system = self.main_heating_systems[0]
                    heating_system_str = "main_heating_systems"
                case HotWaterSource.FROM_SECONDARY_SYSTEM:
                    if self.secondary_heating_systems is None:
                        raise ValueError(
                            f"secondary_heating_systems is not defined, but hot_water_systems[{i}].source='{hot_water_system.source}'"
                        )
                    heating_system = self.secondary_heating_systems[0]
                    heating_system_str = "secondary_heating_systems"
                case _:  # pragma: no cover
                    # validate_hot_water_systems() should catch these cases.
                    continue
            if DomesticEnergyEndUse.HOT_WATER not in heating_system.efficiency:
                raise ValueError(
                    f"hot_water_systems[{i}].source='{hot_water_system.source}' but "
                    f"neither hot_water_systems[{i}].efficiency nor "
                    f"{heating_system_str}[0].efficiency contains "
                    f"'{DomesticEnergyEndUse.HOT_WATER}'"
                )

        return self


class Occupancy(pydantic.BaseModel):
    occupants_adults: int | None = pydantic.Field(ge=1, default=None)
    occupants_children: int | None = pydantic.Field(ge=0, default=None)
    occupancy_schedule: simulation_enums.OccupancySchedule = (
        simulation_enums.OccupancySchedule.EVENINGS_AND_MOST_WEEKENDS
    )
    heating_schedule: simulation_enums.OccupancySchedule | None = pydantic.Field(
        description="""
        Heating schedule.
        Defaults is to use the 'occupancy_schedule' if not set/null.
        """,
        default=None,
    )
    annual_electricity_usage: int | None = pydantic.Field(
        gt=0,
        default=None,
        description="""
        Annual electricity consumption, in kWh.
        """,
    )
    annual_energy_heating: int | None = pydantic.Field(
        gt=0,
        default=None,
        description="""
        Annual gas consumption, in kWh.
        """,
    )
