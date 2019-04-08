"""Fetch and parse Toggl report."""
import datetime
import os
import typing
from dataclasses import dataclass
from decimal import Decimal
from operator import attrgetter

from toggl.api_client import TogglClientApi

from reports.exceptions import TogglError


@dataclass
class TogglParams:
    """Toggl API parameters."""
    workspace_id: str
    token: str
    user_agent: str
    client_ids: str

    @property
    def client_ids_list(self):
        """Get Client IDs to include as a list of strings."""
        return [int(cid) for cid in self.client_ids.split(',')]

    @staticmethod
    def from_env():
        """Build ``TogglParams`` from system environment."""
        return TogglParams(
            workspace_id=os.environ['TOGGL_WORKSPACE_ID'],
            token=os.environ['TOGGL_TOKEN'],
            user_agent=os.environ['TOGGL_USER_AGENT'],
            client_ids=os.environ['TOGGL_CLIENT_IDS']
        )


def _to_human_time(millis):
    seconds = Decimal(millis) / Decimal(1_000)

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return ':'.join(
        [format(int(unit), '02d') for unit in [hours, minutes, seconds]]
    )


@dataclass
class Entry:
    """Toggl project entry."""
    title: str
    time_millis: int

    @property
    def time_human(self):
        """Get human readable time spent on the task, as HH:MM:SS."""
        return _to_human_time(self.time_millis)


@dataclass
class Project:
    """Toggl project."""
    name: str
    entries: typing.List[Entry]


@dataclass
class Report:
    """Toggl report."""
    time_millis: int
    projects: typing.List[Project]

    @property
    def time_human(self):
        """Get human readable time spent on all projects, as HH:MM:SS."""
        return _to_human_time(self.time_millis)


class _ReportCollector:  # pylint: disable=too-few-public-methods
    def __init__(self, toggl_params: TogglParams) -> None:
        super().__init__()
        self._toggl_params = toggl_params
        self._client = TogglClientApi({
            'token': toggl_params.token,
            'user_agent': toggl_params.user_agent,
            'workspace_id': toggl_params.workspace_id
        })

    def fetch(self, since: datetime.date, until: datetime.date) -> Report:
        """Fetch and parse Toggl report."""

        client_ids = self._toggl_params.client_ids_list
        project_names_by_id = {
            project['id']: project['name'] for project in self._projects()
            if project['cid'] in client_ids
        }
        summary = self._summary(since, until)

        projects = []
        total_time_millis = 0
        for project in summary['data']:
            project_id = project['id']
            if project_id not in project_names_by_id:
                continue

            total_time_millis += project['time']
            project_name = project_names_by_id[project_id]
            entries = []

            for item in project['items']:
                entry = Entry(
                    title=item['title']['time_entry'],
                    time_millis=item['time']
                )
                entries.append(entry)

            projects.append(Project(
                name=project_name,
                entries=sorted(
                    entries, key=attrgetter('time_millis'), reverse=True
                )
            ))

        return Report(
            projects=projects,
            time_millis=total_time_millis
        )

    def _projects(self):
        response = self._client.get_projects()
        return self._json(response)

    def _summary(self, since: datetime.date, until: datetime.date):
        params = {
            'user_agent': self._toggl_params.user_agent,
            'workspace_id': self._toggl_params.workspace_id,
            'since': str(since),
            'until': str(until),
            'grouping': 'projects',
            'subgrouping': 'time_entries',
        }
        response = self._client.query_report('/summary', params=params)
        return self._json(response)

    @staticmethod
    def _json(response):
        json = response.json()
        if response.status_code != 200:
            raise TogglError(
                'Cannot perform Toggl request: {}'.format(json))
        return json


def fetch(
        since: datetime.date,
        until: datetime.date,
        toggl_params: TogglParams
) -> Report:
    """Fetch and parse Toggl report."""
    report = _ReportCollector(toggl_params)
    return report.fetch(since, until)
