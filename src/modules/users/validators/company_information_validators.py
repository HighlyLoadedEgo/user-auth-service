import petrovna
import structlog

from src.core.common.exceptions import BadRequestError
from src.modules.users.dtos.companies_dtos import (
    CompanyCreateInformationDTO,
    CompanyInformationDTO,
)

logger = structlog.stdlib.get_logger(__name__)


def validate_company_info(
    company_info: CompanyCreateInformationDTO | CompanyInformationDTO,
) -> bool:
    """Validate company info"""
    try:
        if not petrovna.validate_inn(company_info.tin):
            raise BadRequestError(info="Bad tin number.")
        if not petrovna.validate_kpp(company_info.rrc):
            raise BadRequestError(info="Bad rcc number.")
    except BadRequestError:
        logger.warning("[Common] Invalid company information.")
        raise
    return True


def validate_company_info_exists(
    company_info: CompanyCreateInformationDTO | None,
) -> bool:
    """Validate company info"""

    if not company_info:
        logger.warning("[Common] Company info is empty.")
        raise BadRequestError(info="Company info is empty.")
    return True
