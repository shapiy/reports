"""AWS Lambda handler."""
import datetime
import json
import logging

from reports import formats, mail, report_collector

LOGGER = logging.getLogger()


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """AWS Lambda handler function."""
    LOGGER.setLevel(logging.INFO)
    LOGGER.info('Handler invoked')
    LOGGER.info('Event: %s', event)

    today = datetime.date.today()
    since = today - datetime.timedelta(days=7)
    until = today - datetime.timedelta(days=1)

    toggl_params = report_collector.TogglParams.from_env()
    mail_params = mail.MailParams.from_env()

    report = report_collector.fetch(since, until, toggl_params)
    report_html = formats.to_html(report, since, until)
    mail.send(report_html, mail_params)

    LOGGER.info('Done')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'workspace_id': int(toggl_params.workspace_id),
            'client_ids': toggl_params.client_ids_list,
            'mail_to': mail_params.to_emails_list,
            'mail_cc': mail_params.cc_list
        })
    }


# Entry point for local testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    lambda_handler({}, {})
