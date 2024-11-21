from fastapi_mail import (
    MessageSchema,
    MessageType,
)

from src.core.database.session_context import async_session_context
from src.core.mailing.mail_app import mail_app
from src.modules.users.common.constants import admin_role_list
from src.modules.users.repositories.user_repository import UserRepository


async def send_email(
    subject: str,
    recipients: list[str],
    body: str,
    template_name: str | None = None,
) -> None:
    """Send mail function."""
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html,
    )
    fm = mail_app()
    await fm.send_message(
        message=message,
        template_name=template_name,
    )


async def send_notify_new_admin_signup_mail() -> None:
    """Send notify new admin signup email to admins."""
    subject = "LYNX | Новая регистрация"
    body = """
    На сайте LYNX зарегистрировался новый пользователь, зайдите в админскую панель для дальнейшего одобрения.
    Пользователь: Сотрудник
    """
    async with async_session_context() as session:
        user_repo = UserRepository(session=session)
        admins = await user_repo.get_users_by_roles(roles_list=admin_role_list)
    recipients = [admin.email for admin in admins]
    if not len(recipients):
        return
    await send_email(
        subject=subject,
        recipients=recipients,
        body=body,
    )


async def send_notify_new_company_signup_mail() -> None:
    """Send notify new admin signup email to admins."""
    subject = "LYNX | Новая регистрация"
    body = """
    На сайте LYNX зарегистрировался новый пользователь, зайдите в админскую панель для дальнейшего одобрения.
    Пользователь: Юредическое лицо
    """
    async with async_session_context() as session:
        user_repo = UserRepository(session=session)
        admins = await user_repo.get_users_by_roles(roles_list=admin_role_list)
    recipients = [admin.email for admin in admins]
    if not len(recipients):
        return
    await send_email(
        subject=subject,
        recipients=recipients,
        body=body,
    )


async def send_admin_confirm_mail(
    recipient: str,
    token: str,
) -> None:
    """Send confirmation user email message."""
    subject = "Lynx 2.0 email confirmation."
    link = "http://37.230.192.154:8000/api/v1/admin/auth/confirm?token=" + token
    body = f"""
    Здравствуйте,

    Вы недавно зарегистрировались на сайте Example.com, и нам нужно подтвердить ваш адрес электронной почты, чтобы завершить процесс регистрации.

    Пожалуйста, перейдите по следующей ссылке для подтверждения вашего адреса электронной почты и активации вашего аккаунта: {link}

    Если вы не регистрировались на сайте Example.com, пожалуйста, проигнорируйте это письмо.

    С уважением, Lynx.
    Компания lynx.com
    lynx@intehnika.ru
    """
    await send_email(
        subject=subject,
        recipients=[recipient],
        body=body,
    )


async def send_user_confirm_mail(
    recipient: str,
    token: str,
) -> None:
    """Send confirmation user email message."""
    subject = "Lynx 2.0 email confirmation."
    link = "http://37.230.192.154:8000/api/v1/web/auth/confirm?token=" + token
    body = f"""
    Здравствуйте,

    Вы недавно зарегистрировались на сайте Example.com, и нам нужно подтвердить ваш адрес электронной почты, чтобы завершить процесс регистрации.

    Пожалуйста, перейдите по следующей ссылке для подтверждения вашего адреса электронной почты и активации вашего аккаунта: {link}

    Если вы не регистрировались на сайте Example.com, пожалуйста, проигнорируйте это письмо.

    С уважением, Lynx.
    Компания lynx.com
    lynx@intehnika.ru
    """
    await send_email(
        subject=subject,
        recipients=[recipient],
        body=body,
    )
