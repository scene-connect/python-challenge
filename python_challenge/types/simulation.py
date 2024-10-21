import functools
from abc import ABC
from decimal import Decimal
from typing import Annotated
from typing import Any
from typing import Literal
from typing import NamedTuple

import pydantic
from geojson_pydantic import Point

from .epc_enums import HeatingControlMethod
from .epc_enums import HeatingSystemEmitter
from .epc_enums import HeatingSystemSource
from .epc_enums import MeterType
from .simulation_enums import DomesticEnergyEndUse
from .simulation_enums import EnergySource
from .simulation_enums import HotWaterSource
from .simulation_enums import InsulationMaterial
from .simulation_enums import SolarPVTracking


class ModelSettings(pydantic.BaseModel, ABC):
    pass


class SolarPVArray(pydantic.BaseModel):
    """
    Configuration of a Solar PV array, without location, for use in Home object.
    """

    peak_power: float = pydantic.Field(
        title="Peak Power (kWp)",
        description="The peak power capacity of this PV system (in KiloWatts)",
        gt=0,
    )
    inverter_power: float | None = pydantic.Field(
        title="Inverter power capacity (kW)",
        description="""
        AC inverter capacity in KiloWatts. If not given, the peak_power capacity is
        assumed to be equal to AC inverter capacity.
        """,
        gt=0,
        default=None,
    )
    tilt: int = pydantic.Field(
        title="Tilt angle (degrees)",
        description="""
        The tilt angle of the array in degrees from horizontal.
        0 is horizontal, 90 is vertical.
        """,
        ge=0,
        le=90,
        default=35,
    )
    azimuth: int = pydantic.Field(
        title="Azimuth (degrees)",
        description="""
        The orientation of the panel relative to north, measures clockwise in degrees
        (North=0).
        """,
        ge=0,
        lt=360,
        default=180,  # south
    )
    tracking: SolarPVTracking | None = pydantic.Field(
        description="Whether a sun tracking system is in use.",
        default=None,
    )
    age: int = pydantic.Field(
        title="System age (years)",
        ge=0,
        default=0,
    )


class SolarPVModelSettings(SolarPVArray, ModelSettings):
    """
    Internal Solar PV  model settings.

    Includes location (which we will populate from the Home object) and advanced fields
    which we should not expose to partners (degradation).
    """

    location: Point = pydantic.Field(
        title="Geographic location of the PV array (latitude, longitude)",
    )
    system_losses: float = pydantic.Field(
        title="System losses",
        description="Additional system losses not caused by panel and inverter.",
        gt=0,
        le=1,
        default=0.1,
    )
    degrade_performance_by_age: bool = pydantic.Field(
        description="Whether to degrade original peak power output by age.",
        default=True,
    )
    degradation_initial: float = pydantic.Field(
        description="Initial panel degradation drop in the first year (percentage).",
        ge=0,
        lt=1,
        default=0.025,  # 2.5%
    )
    degradation_rate: float = pydantic.Field(
        description="Average annual panel degradation (percentage).",
        ge=0,
        lt=1,
        default=0.005,  # 0.5%
    )

    @functools.cached_property
    def peak_power_adjusted(self) -> float:
        peak_power = self.peak_power
        if self.degrade_performance_by_age:
            peak_power *= 1 - self.degradation_for_age
        return peak_power

    @functools.cached_property
    def degradation_for_age(self) -> float:
        if self.age == 0:
            return 0
        return self.degradation_initial + ((self.age - 1) * self.degradation_rate)

    @functools.cached_property
    def peak_power_watts(self) -> float:
        return self.peak_power_adjusted * 1000

    @functools.cached_property
    def inverter_power_watts(self) -> float:
        if self.inverter_power:
            return self.inverter_power * 1000
        # Use non-degraded peak-power, inverter performance doesn't degrade like panels.
        return self.peak_power * 1000


def _validate_monthly_dict(value: dict[int, Any]):
    if len(value) != 12:
        raise ValueError(
            f"Expected exactly 12 floats for monthly efficiencies, got: {len(value)}"
        )
    month_range = range(1, 13)
    for key in value.keys():
        if key not in month_range:
            raise ValueError(f"Month {key} missing from monthly dict: {value.keys()}")
    return value


def _validate_efficiency(value: float):
    if value <= 0:
        raise ValueError(f"Efficiency values must be greater than zero, got: {value}")
    return value


FlatEfficiency = Annotated[float, pydantic.AfterValidator(_validate_efficiency)]


class SummerWinterEfficiency(NamedTuple):
    summer: FlatEfficiency
    winter: FlatEfficiency


MonthlyEfficiency = Annotated[
    dict[int, FlatEfficiency], pydantic.AfterValidator(_validate_monthly_dict)
]

Efficiency = FlatEfficiency | SummerWinterEfficiency | MonthlyEfficiency

DOC_EFFICIENCY = """
Efficiency can either be provided as:

 - A single float, for a flat average efficiency.
 - A pair of floats, for summer/winter efficiencies.
 - An array of monthly efficiencies, keyed by month number.
"""


class BoilerProperties(pydantic.BaseModel):
    system_type: Literal["boiler"] = "boiler"
    condensing: bool | None = None
    combination: bool | None = None
    back_boiler: bool | None = None
    # In future we will add more details to model, such as peak-output.


class HeatPumpProperties(pydantic.BaseModel):
    system_type: Literal["heat_pump"] = "heat_pump"
    output_power: Decimal | None = pydantic.Field(
        title="Heat output power (kW)",
        description="""
        This is an estimate of the heat output power required for the home.
        It is calculated the modelled heat demand for the home.
        """,
        default=None,
    )
    # In future we will add more details to model, such as peak-power/output,
    # COP curves, etc..


class _BaseHeatingSystem(pydantic.BaseModel):
    source_properties: BoilerProperties | HeatPumpProperties | None = pydantic.Field(
        description="""
            Specific appliance properties.
            Most are not directly available in the EPC and these will be assumed using
            SAP 10 or other methodologies based on what information is available.
            """,
        default=None,
        discriminator="system_type",
    )
    energy_source: EnergySource | None = None
    efficiency: dict[DomesticEnergyEndUse, Efficiency] = pydantic.Field(
        description=f"""
        Efficiency of the heat source, by DomesticEnergyEndUse.

        {DOC_EFFICIENCY}
        """,
        default={},
    )
    age: int = pydantic.Field(
        description="""
        Age of the appliance, in years. Estimated from the EPC assessment date.
        Default 0 for new.
        """,
        ge=0,
        default=0,
    )


class HeatingSystem(_BaseHeatingSystem):
    source: HeatingSystemSource | None = None
    emitters: list[HeatingSystemEmitter] = []

    @property
    def is_wet(self) -> bool | None:
        """
        Estimate of whether the heating system is a "wet" (hydronic) system.
        None if unsure/unknown.
        """
        if not self.source:
            return None

        # Definitely wet:
        if self.source in (HeatingSystemSource.BOILER,):
            return True

        # Definitely not wet.
        if self.source in (
            HeatingSystemSource.ELECTRIC_UNDERFLOOR_HEATERS,
            HeatingSystemSource.CEILING_HEATING,
            HeatingSystemSource.STORAGE_HEATERS,
            HeatingSystemSource.EXHAUST_AIR_MEV_SOURCE_HEAT_PUMP,
            HeatingSystemSource.PORTABLE_HEATERS,
        ):
            return False

        # Definitely not wet:
        if self.emitters == [HeatingSystemEmitter.WARM_AIR]:
            return False

        # Definitely wet
        if (
            HeatingSystemEmitter.RADIATORS in self.emitters
            or HeatingSystemEmitter.UNDERFLOOR in self.emitters
        ) and self.source in [
            HeatingSystemSource.AIR_SOURCE_HEAT_PUMP,
            HeatingSystemSource.GROUND_SOURCE_HEAT_PUMP,
            HeatingSystemSource.WATER_SOURCE_HEAT_PUMP,
            HeatingSystemSource.COMMUNITY_SCHEME,
            HeatingSystemSource.COMMUNITY_SCHEME_RECOVERED_HEAT_FROM_BOILERS,
            HeatingSystemSource.ROOM_HEATERS,  # With a heating coil to radiators
        ]:
            return True

        return None


class HeatingControlSystem(pydantic.BaseModel):
    control_methods: list[HeatingControlMethod] = pydantic.Field(
        description="Control methods(s)/devices(s) used by the main heating system(s)"
    )


class HotWaterTank(pydantic.BaseModel):
    volume: int | None = pydantic.Field(
        description="Tank size (litres)",
        gt=0,
        default=None,
    )
    insulation_thickness: int | None = None
    insulation_material: InsulationMaterial | None = None
    has_thermostat: bool | None = pydantic.Field(
        description="Does the hot water tank/cylinder have a thermostat?",
        default=None,
    )


class ImmersionHeaterProperties(pydantic.BaseModel):
    system_type: Literal["immersion_heater"] = "immersion_heater"
    power: float = pydantic.Field(
        description="Power rating (kW)",
        gt=0,
        default=3.0,
    )


class RangeCookerHotWaterProperties(pydantic.BaseModel):
    system_type: Literal["range_cooker"] = "range_cooker"
    automatic_ignition: bool | None = None


class HotWaterSystem(_BaseHeatingSystem):
    source: HotWaterSource | None = None
    storage: HotWaterTank | None = None
    source_properties: (
        BoilerProperties
        | HeatPumpProperties
        | ImmersionHeaterProperties
        | RangeCookerHotWaterProperties
        | None
    ) = pydantic.Field(
        description="""
        Specific appliance properties.

        Most are not directly available in the EPC and these will be assumed using
        SAP 10 or other methodologies based on what information is available.

        If source is from main or secondary system, then this can be left unset and
        ZUoS will select the first wet main/secondary heating system.
        If multiple main/secondary wet heating systems exist, this can be used to
        specify the efficiency of the hot water to avoid ZUoS selecting the wrong
        system.
        """,
        default=None,
        discriminator="system_type",
    )


class HeatingEfficiencyModelSettings(ModelSettings):
    efficiency: dict[DomesticEnergyEndUse, Efficiency]


class HeatingMeterType(pydantic.BaseModel):
    meter_type: MeterType = pydantic.Field(
        description="Meter type of the main heating system(s)"
    )
