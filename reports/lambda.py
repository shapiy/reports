"""AWS Lambda handler."""
import datetime
import json
import logging

from reports.exceptions import ReportsError, SendGridError, TogglError
from reports import formats, mail, report_collector

LOGGER = logging.getLogger()


def lambda_handler(event, context):  # pylint: disable=unused-argument
    """AWS Lambda handler function."""
    try:
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
    except SendGridError as error:
        LOGGER.exception('Failed to send email')
        return {
            'statusCode': 500,
            'error': error.description
        }
    except TogglError as error:
        LOGGER.exception('Failed to fetch Toggl report')
        return {
            'statusCode': 500,
            'error': error.description
        }
    except ReportsError as error:
        LOGGER.exception('Failed')
        return {
            'statusCode': 500,
            'error': error.description
        }
    except Exception:   # pylint: disable=broad-except
        LOGGER.exception('Unknown error')
        return {
            'statusCode': 500,
            'error': 'Unknown error, check Lambda logs'
        }


# Entry point for local testing
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    lambda_handler({}, {})
