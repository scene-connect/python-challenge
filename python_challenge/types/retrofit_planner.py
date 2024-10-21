from uuid import UUID

import pydantic

from .home import EnergyProfile
from .home import Home
from .home import Occupancy
from .recommendations import ImprovementEnergyProfile


class RetrofitPlannerResponsePublic(pydantic.BaseModel):
    """
    Public API response for a Home energy profile and retrofit plan.
    """

    simulation_id: UUID
    baseline_energy_profile: EnergyProfile
    baseline_home: Home = pydantic.Field(
        description="""
        The home configuration used to model the baseline, before any improvements.
        """,
    )
    occupancy_profile: Occupancy = pydantic.Field(
        description="""
        The occupancy configuration used for modelling the Home.
        """
    )
    improvement_option_evaluation: list[ImprovementEnergyProfile] = pydantic.Field(
        description="""
        Unordered list of individual improvements and their energy impacts, compared
        to the baseline.

        This corresponds to the PAS2035 IOE (Improvement Option Evaluation) with reports
        on each individual improvement option, in isolation.

        Note: These individual improvements are each relative to the baseline, with no
        other improvements applied, and so may differ from the final "improvement_plan"
        (MTIP) which considers the improvements in order.
        In particular space heating requirements will likely be significantly different
        when improvements are applied in order, which can impact the sizing (and costs)
        of heating appliances such as heat pumps.
        """
    )
    improvement_plan: list[ImprovementEnergyProfile] = pydantic.Field(
        description="""
        This corresponds to the PAS2035 MTIP (Medium Term Improvement Plan) with
        ordered improvements applied cumulatively.

        Each energy profile represents a stage in the plan, with one or more
        improvements, and each stage's energy impact is calculated relative to the
        previous stage (not relative to the baseline).
        """
    )
