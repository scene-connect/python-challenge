import typing
from copy import deepcopy
from decimal import Decimal
from typing import Annotated
from typing import Literal

import pydantic

from . import simulation_enums
from .home import EnergyProfile
from .home import Home
from .pas2035 import PAS2035_IMPROVEMENT_COMPATIBILITY_RESTRICTIONS
from .pas2035 import PAS2035ImprovementCategory
from .pas2035 import PAS2035ImprovementCategoryMeasuresMap
from .pas2035 import PAS2035ImprovementMeasure
from .recommendation_enums import AdditionalImprovementCategory
from .recommendation_enums import AdditionalImprovementMeasure
from .recommendation_enums import Disruption
from .recommendation_enums import ImprovementMeasureCompatibility
from .recommendation_enums import InstallationTimeframe
from .simulation import HeatingControlSystem
from .simulation import HeatingMeterType
from .simulation import HeatingSystem
from .simulation import HotWaterTank
from .simulation import SolarPVArray
from .simulation_enums import InsulationMaterial

# Combined type to save typing both in our type hints.
T_ImprovementMeasure = PAS2035ImprovementMeasure | AdditionalImprovementMeasure
T_ImprovementCategory = PAS2035ImprovementCategory | AdditionalImprovementCategory

T_ImprovementMeasuresMap = dict[
    T_ImprovementCategory,
    set[T_ImprovementMeasure],
]

_AdditionalImprovementCategoryMeasuresMap: typing.Final[T_ImprovementMeasuresMap] = {
    PAS2035ImprovementCategory.RENEWABLES: {
        AdditionalImprovementMeasure.BATTERY,
    },
    PAS2035ImprovementCategory.DISTRIBUTION: {
        AdditionalImprovementMeasure.WET_UNDER_FLOOR_HEATING,
    },
}


def _built_full_category_measures_map() -> T_ImprovementMeasuresMap:
    map: T_ImprovementMeasuresMap = deepcopy(
        PAS2035ImprovementCategoryMeasuresMap
    )  # type:ignore[reportAssignmentType]
    for category, measures in _AdditionalImprovementCategoryMeasuresMap.items():
        map[category].update(measures)
    return map


# Combined map, use this in our code.
ImprovementCategoryMeasuresMap: typing.Final[T_ImprovementMeasuresMap] = (
    _built_full_category_measures_map()
)


AllImprovementMeasures: typing.Final[list[T_ImprovementMeasure]] = list(
    PAS2035ImprovementMeasure
) + list(AdditionalImprovementMeasure)

T_ImprovementMeasureCompatibilityMap = dict[
    T_ImprovementMeasure, dict[T_ImprovementMeasure, ImprovementMeasureCompatibility]
]

ADDITIONAL_IMPROVEMENT_COMPATIBILITY_RESTRICTIONS: (
    T_ImprovementMeasureCompatibilityMap
) = {
    AdditionalImprovementMeasure.BATTERY: {
        PAS2035ImprovementMeasure.SOLAR_PHOTOVOLTAICS: ImprovementMeasureCompatibility.SPECIFICATION_REQUIRED,
    },
    AdditionalImprovementMeasure.WET_UNDER_FLOOR_HEATING: {
        PAS2035ImprovementMeasure.RADIATOR_PANELS: ImprovementMeasureCompatibility.NEED_CONSTRUCTION_DETAIL,
        PAS2035ImprovementMeasure.AIR_SOURCE_HEAT_PUMP: ImprovementMeasureCompatibility.SPECIFICATION_REQUIRED,
        PAS2035ImprovementMeasure.GROUND_SOURCE_HEAT_PUMP: ImprovementMeasureCompatibility.SPECIFICATION_REQUIRED,
        PAS2035ImprovementMeasure.BOILER_REPLACEMENT: ImprovementMeasureCompatibility.SPECIFICATION_REQUIRED,
    },
}

ALL_IMPROVEMENT_MEASURES_COMPATIBILITY_RESTRICTIONS: typing.Final[
    T_ImprovementMeasureCompatibilityMap
] = (
    ADDITIONAL_IMPROVEMENT_COMPATIBILITY_RESTRICTIONS
    | PAS2035_IMPROVEMENT_COMPATIBILITY_RESTRICTIONS
)  # type: ignore[AssignmentType]  # This IS type-compatible but pyright can't see it.


class RecommendationsSettings(pydantic.BaseModel):
    """
    Settings for the recommendations engine.
    """

    exclude_improvement_measures: list[T_ImprovementMeasure] = pydantic.Field(
        default=[],
        description="""
        List of measures to exclude from the recommendations.
        Use this if certain measures are not suitable to the home or are unacceptable
        to the occupant.
        """,
    )


class ImprovementFunding(pydantic.BaseModel):
    amount: int | tuple[int, int]
    title: str
    description: str


class InsulationImprovementSpecifications(pydantic.BaseModel):
    specification_type: Literal["insulation_improvement"] = "insulation_improvement"
    u_value: Decimal | None = pydantic.Field(
        description="Target U-value (W/m2K) to improve to.", default=None
    )
    insulation_thickness: int | None = pydantic.Field(
        description="Insulation thickness (mm)", default=None
    )
    insulation_material: InsulationMaterial | None = None


class WindowImprovementSpecifications(pydantic.BaseModel):
    specification_type: Literal["window_improvement"] = "window_improvement"
    u_value: Decimal | None = pydantic.Field(
        description="Target U-value (W/m2K) to improve windows to.", default=None
    )
    from_window_type: simulation_enums.WindowGlazingType | None = pydantic.Field(
        description="Windows of which glazing type to upgrade.", default=None
    )
    to_window_type: simulation_enums.WindowGlazingType = pydantic.Field(
        description="Glazing type to improve the windows to."
    )
    multiple_glazing_percentage: int = pydantic.Field(
        description="The target percentage of windows that is multiple-glazed",
        le=100,
        ge=0,
    )
    windows_construction: simulation_enums.WindowConstruction | None = pydantic.Field(
        description="",
        default=None,
    )
    windows_glazing_gap: simulation_enums.WindowGlazingGap | None = pydantic.Field(
        description="",
        default=None,
    )


class EfficientLightingSpecification(pydantic.BaseModel):
    specification_type: Literal["efficient_lighting"] = "efficient_lighting"
    low_energy_lighting_percentage: float | None = pydantic.Field(
        description="Target percentage of fixed lighting outlets with low energy lighting",
        default=None,
        ge=0,
        le=100,
    )


class DoorImprovementSpecifications(pydantic.BaseModel):
    specification_type: Literal["door_improvement"] = "door_improvement"
    u_value: Decimal | None = pydantic.Field(
        description="Target U-value (W/m2K) for new or replacement external doors.",
        default=None,
    )


class DraughtProofingSpecifications(pydantic.BaseModel):
    specification_type: Literal["draught_proofing"] = "draught_proofing"
    draught_proofed_percentage: int = pydantic.Field(
        description="% of windows/doors that has been draught proofed.",
        le=100,
        ge=0,
    )


class HeatingSystemSpecifications(HeatingSystem):
    specification_type: Literal["heating_system"] = "heating_system"


class HeatingControlSystemSpecifications(HeatingControlSystem):
    specification_type: Literal["heating_control_system"] = "heating_control_system"


class HotWaterTankSpecifications(HotWaterTank):
    specification_type: Literal["hot_water_tank"] = "hot_water_tank"


class HeatingMeteterTypeSpecifications(HeatingMeterType):
    specification_type: Literal["heating_meter_type"] = "heating_meter_type"


class SolarPVArraySpecifications(SolarPVArray):
    specification_type: Literal["solar_pv_array"] = "solar_pv_array"


T_ImprovementSpecifications = Annotated[
    (
        SolarPVArraySpecifications
        | InsulationImprovementSpecifications
        | HeatingSystemSpecifications
        | HeatingControlSystemSpecifications
        | WindowImprovementSpecifications
        | DoorImprovementSpecifications
        | DraughtProofingSpecifications
        | HotWaterTankSpecifications
        | EfficientLightingSpecification
        | HeatingMeteterTypeSpecifications
    ),
    pydantic.Field(discriminator="specification_type"),
]


class Improvement(pydantic.BaseModel):
    category: T_ImprovementCategory
    measure: T_ImprovementMeasure
    specification: (
        T_ImprovementSpecifications | list[T_ImprovementSpecifications] | None
    ) = pydantic.Field(
        description="""
        Specifications of the improvement (e.g. materials, dimensions).

        The structure of this varies for each improvement measure.

        ZUoS attempt document the specific improvements which we model, but some
        measures may not have specific details, such as
        "Draught-proofing and air-tightness".
        """,
        # Devs: Define a pydantic model for each improvement measure with all relevant
        # details, and add it to T_ImprovementSpecifications. Some measures may share
        # a specification, e.g. boiler upgrades (regardless of fuel source).
        # they are distinguished based on their specification_type field.
        default=None,
    )
    capital_cost: tuple[int, int] | None = pydantic.Field(
        description="""
        A cost range for this improvement measure, in £ GBP.
        This is scaled to the home.
        """,
        default=None,
    )
    embodied_carbon: tuple[int, int] | None = pydantic.Field(
        description="""
        NOT CURRENTLY IMPLEMENTED.
        """,
        default=None,
    )


class ImprovementDetails(Improvement):
    run_model: bool = pydantic.Field(
        description="Sets whether or not we will run additional models for the improvement.",
        default=True,
    )
    funding: list[ImprovementFunding] = pydantic.Field(
        description="""
        Funding options available for this improvement.
        NOT CURRENTLY IMPLEMENTED.
        """,
        default=[],
    )
    installation_disruption: Disruption
    installation_time: InstallationTimeframe
    community_potential: bool | None = pydantic.Field(
        description="""
        Is this improvement relevant for other properties in the community?
        """,
        default=None,
    )
    required_measures: list[T_ImprovementMeasure] = pydantic.Field(
        description="""
        Other measures which must be performed before this improvement.

        In addition the order of ZUoS recommendations, this field lists dependent
        measures which must (or are very likely to be) carried out before or alongside
        this improvement.

        This list is not tailored to the home, e.g. we may "require" radiator upgrades
        for heat pumps, when a home may have recently had upgraded radiators already.
        """,
        default=[],
    )
    compatibility: dict[T_ImprovementMeasure, ImprovementMeasureCompatibility] = (
        pydantic.Field(
            description="""
        Other measures which may have compatibility considerations with this measure,
        and the severity of their interaction.
        Measures which are compatible (with no interaction) are not listed.
        """,
            default={},
        )
    )
    notes: list[str] = pydantic.Field(
        description="""Additional notes and limitations to consider before recommending the improvement.""",
        default=[],
    )

    @property
    def description(self) -> str:
        return f"{self.category} {self.measure}"


class ImprovementEnergyProfile(pydantic.BaseModel):
    improvements: list[Improvement | ImprovementDetails] = pydantic.Field(
        description="List of improvements to apply together in this set."
    )
    improved_home: Home = pydantic.Field(
        description="New Home object with the improvement(s) applied."
    )
    energy_profile: EnergyProfile = pydantic.Field(
        description="""
        Full energy profile of the home with this set of improvements applied.
        """
    )
    relative_energy_change: EnergyProfile = pydantic.Field(
        description="""
        The difference from the home with and without these improvements.
        Values are relative, and should be negative for reductions.

        In IOE this is relative to the baseline.
        In MTIP this is relative to the previous stage.
        """
    )
    payback_years: tuple[int | None, int | None] = pydantic.Field(
        description="""
        Payback period for this set of improvements, as a range in years.
        If the payback period is negative, the values are (None, None).

        Note: This is only for this set of improvements. Savings from previous stages
        in the MTIP will not contribute towards the packback period of this improvement
        set.
        """
    )
