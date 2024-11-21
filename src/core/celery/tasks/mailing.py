import asyncio

import structlog

from src.core.mailing.messages import (
    send_admin_confirm_mail,
    send_notify_new_admin_signup_mail,
    send_notify_new_company_signup_mail,
    send_user_confirm_mail,
)

logger = structlog.stdlib.get_logger(__name__)


def send_admin_confirm_mail_task(
    recipient: str,
    token: str,
) -> None:
    """Send confirmation user email message task."""
    logger.info("[Celery] Running task to send admin confirm email.")
    asyncio.get_event_loop().run_until_complete(
        send_admin_confirm_mail(
            recipient=recipient,
            token=token,
        ),
    )


def send_notify_new_admin_signup_mail_task() -> None:
    """Send confirmation user email message task."""
    logger.info("[Celery] Running task to send notify about new admin.")
    asyncio.get_event_loop().run_until_complete(send_notify_new_admin_signup_mail())


def send_notify_new_company_signup_mail_task() -> None:
    """Send confirmation user email message task."""
    logger.info("[Celery] Running task to send notify about new company.")
    asyncio.get_event_loop().run_until_complete(send_notify_new_company_signup_mail())


def send_user_confirm_mail_task(
    recipient: str,
    token: str,
) -> None:
    """Send confirmation user email message task."""
    logger.info("[Celery] Running task to send user confirm email.")
    asyncio.get_event_loop().run_until_complete(
        send_user_confirm_mail(
            recipient=recipient,
            token=token,
        ),
    )
