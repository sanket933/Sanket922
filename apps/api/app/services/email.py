import imaplib
import smtplib
import ssl
from email.message import EmailMessage
from app.core.config import get_settings


class HostingerEmailClient:
    def __init__(self):
        self.settings = get_settings()

    def send_email(self, to_email: str, subject: str, body: str, reply_to: str | None = None) -> None:
        if not self.settings.smtp_password:
            raise RuntimeError('SMTP_PASSWORD is required and must be configured as a backend secret')
        message = EmailMessage()
        message['From'] = self.settings.smtp_username
        message['To'] = to_email
        message['Subject'] = subject
        if reply_to:
            message['Reply-To'] = reply_to
        message.set_content(body)
        context = ssl.create_default_context()
        if self.settings.smtp_use_ssl:
            with smtplib.SMTP_SSL(self.settings.smtp_host, self.settings.smtp_port, context=context) as server:
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.send_message(message)
        else:
            with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_fallback_port) as server:
                server.starttls(context=context)
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.send_message(message)

    def fetch_recent_replies(self, mailbox: str = 'INBOX', limit: int = 25) -> list[dict[str, str]]:
        if not self.settings.imap_password:
            raise RuntimeError('IMAP_PASSWORD is required and must be configured as a backend secret')
        with imaplib.IMAP4_SSL(self.settings.imap_host, self.settings.imap_port) as mail:
            mail.login(self.settings.imap_username, self.settings.imap_password)
            mail.select(mailbox)
            _, data = mail.search(None, 'UNSEEN')
            ids = data[0].split()[-limit:]
            replies = []
            for msg_id in ids:
                _, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE MESSAGE-ID)])')
                replies.append({'id': msg_id.decode(), 'headers': msg_data[0][1].decode(errors='ignore')})
            return replies
