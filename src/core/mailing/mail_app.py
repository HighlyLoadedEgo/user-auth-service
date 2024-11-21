from fastapi_mail import (
    ConnectionConfig,
    FastMail,
)

from src.config.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAILING.SMTP_USER,
    MAIL_PASSWORD=settings.MAILING.SMTP_PASSWORD,
    MAIL_FROM=settings.MAILING.SMTP_USER,
    MAIL_PORT=settings.MAILING.SMTP_PORT,
    MAIL_SERVER=settings.MAILING.SMTP_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    # TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


def mail_app() -> FastMail:
    """Init FastMail app."""
    fm = FastMail(conf)

    return fm
