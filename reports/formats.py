"""Time report formats."""
import datetime

from jinja2 import Environment, PackageLoader, select_autoescape

from reports import report_collector


def to_html(
        report: report_collector.Report,
        since: datetime.date,
        until: datetime.date
) -> str:
    """Format time report to HTML using Jinja ``email.html`` template."""
    env = Environment(
        loader=PackageLoader('reports', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('email.html')
    return template.render(report=report, since=since, until=until)
