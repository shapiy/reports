"""Send time report via email using Sendgrid."""
import os
from dataclasses import dataclass

from python_http_client import HTTPError
from sendgrid import SendGridAPIClient, Mail

from reports.exceptions import SendGridError

DEFAULT_MAIL_FROM = 'reports@shapiy.github.io'
DEFAULT_MAIL_SUBJECT = 'Weekly report'


@dataclass
class MailParams:
    """Email sending parameters."""
    sendgrid_api_key: str
    from_email: str
    to_emails: str
    cc: str
    subject: str

    @property
    def to_emails_list(self):
        """Get TO addresses to a list of strings."""
        return self.to_emails.split(',')

    @property
    def cc_list(self):
        """Get CC addresses to a list of strings."""
        return self.cc.split(',')

    @staticmethod
    def from_env():
        """Build ``MailParams`` from system environment."""
        return MailParams(
            sendgrid_api_key=os.environ['SENDGRID_API_KEY'],
            from_email=os.environ.get('MAIL_FROM', DEFAULT_MAIL_FROM),
            to_emails=os.environ['MAIL_TO'],
            cc=os.environ.get('MAIL_CC') or '',
            subject=os.environ.get('MAIL_SUBJECT', DEFAULT_MAIL_SUBJECT)
        )


def send(html: str, params: MailParams) -> None:
    """Send email with time report."""
    message = Mail(
        from_email=params.from_email,
        to_emails=params.to_emails_list,
        subject=params.subject,
        html_content=html
    )
    if params.cc_list:
        message.cc = params.cc_list

    client = SendGridAPIClient(params.sendgrid_api_key)
    try:
        client.send(message)
    except HTTPError as exc:
        raise SendGridError('Sendgrid API failure: {}, {}'.format(
            exc.status_code, exc.body)) from exc
