from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.config import CONFIG
from app.utils import Singleton


class MailingService(metaclass=Singleton):
    def __init__(self):
        self._config = ConnectionConfig(
            MAIL_SERVER=CONFIG.mail_server,
            MAIL_USERNAME=CONFIG.mail_username,
            MAIL_PASSWORD=CONFIG.mail_password,
            MAIL_FROM=CONFIG.mail_sender,
            MAIL_PORT=CONFIG.mail_port,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True
        )

        self._mail = FastMail(self._config)

    async def send_verification_email(self, email: str, token: str):
        url = CONFIG.root_url + '/mail/verify/' + token

        if CONFIG.mail_console:
            print("POST to " + url)
        else:
            message = MessageSchema(
                recipients=[email],
                subject="ChampStats | Verificação de email",
                body=f"Seja bem vindo ao ChampStats! Por favor verifique seu email utilizando o link: {url}"
            )

            await self._mail.send_message(message)

    async def send_password_reset_email(self, email: str, token: str):
        url = CONFIG.root_url + '/register/reset-password/' + token
        if CONFIG.mail_console:
            print('POST to ' + url)
        else:
            message = MessageSchema(
                recipients=[email],
                subject="ChampStats | Redefinição de senha",
                body=f"Clique no link para redefinir sua senha: {url}\nNão foi você? Apenas ignore este email"
            )

            await self._mail.send_message(message)
