import os
import re
from datetime import datetime

import pandas as pd
import requests
from django.conf import settings

from core import exceptions


class ExportDataToCsvBehavior:
    export_fields: tuple

    def _get_fields(self):
        columns = []
        fields = {}
        rename = {}
        for f in self.export_fields:
            if isinstance(f, str):
                columns.append(f)
                rename[f] = f
                fields[f] = {'field': f, 'label': f, 'options': {}}
            elif isinstance(f, tuple) or isinstance(f, list):
                columns.append(f[0])
                rename[f[0]] = f[1]
                fields[f[0]] = {'field': f[0], 'label': f[1], 'options': {}}
                if len(f) > 2:
                    fields[f[0]]['options'] = f[2]

        return columns, fields, rename

    @staticmethod
    def _format_duration(seconds: float):
        if not seconds:
            return None

        minutes = int(seconds / 60)
        seconds = int(seconds - minutes * 60)
        hours = int(minutes / 60)
        minutes = int(minutes - hours * 60)

        _format = ('{h:03d}' if hours > 99 else '{h:02d}') + ':{m:02d}:{s:02d}'
        return _format.format(h=hours, m=minutes, s=seconds)

    def _load_options(self, data, fields):
        for f in fields.values():
            try:
                if 'options' in f:
                    _key = f['field']
                    for (_opt_key, _opt_value) in f['options'].items():
                        if _opt_key == 'choices':
                            for _ch in _opt_value:
                                data.loc[data[_key] == _ch[0], _key] = str(_ch[1])
                        elif _opt_key == 'date':
                            if isinstance(_opt_value, str):
                                _ts = pd.to_datetime(data[_key], format=_opt_value)
                                data[_key] = _ts.dt.strftime(_opt_value)
                            elif isinstance(_opt_value, dict):
                                if _opt_value.get('utc'):
                                    _ts = pd.to_datetime(data[_key], format=_opt_value.get('from'), utc=True)
                                    _ts = _ts.dt.tz_convert(tz=settings.TIME_ZONE)
                                else:
                                    _ts = pd.to_datetime(data[_key], format=_opt_value.get('from'))
                                data[_key] = _ts.dt.strftime(_opt_value.get('to', _opt_value.get('from')))
                        elif _opt_key == 'timedelta':
                            if isinstance(_opt_value, bool) and _opt_value is True:
                                _ts = pd.to_timedelta(data[_key]).dt.total_seconds()
                                data[_key] = _ts.map(self._format_duration)
                        elif _opt_key == 'utc':
                            if isinstance(_opt_value, bool) and _opt_value is True:
                                data[_key] = data[_key].dt.tz_convert(tz=settings.TIME_ZONE)
                        elif _opt_key == 'quote':
                            if isinstance(_opt_value, bool) and _opt_value is True:
                                data[_key] = data[_key].apply(lambda x: "'" + str(x) + "'")
                        elif _opt_key == 'formatter':
                            if callable(_opt_value):
                                data[_key] = data[_key].apply(_opt_value)
            except Exception:
                pass
        return data

    def _create_data_frame(self, data=None, queryset=None):
        if not self.export_fields:
            raise exceptions.ActionFailedException(cause='export fields must be declared')

        # get fields to export
        columns, fields, rename = self._get_fields()

        # create data frame
        if queryset:
            queryset = queryset.values(*columns)
            df = pd.DataFrame.from_records(data=queryset, columns=columns, coerce_float=True)
        else:
            df = pd.DataFrame.from_dict(data=data)
            df = df[columns]

        df = self._load_options(df, fields=fields)
        df = df.replace('NaT', '', regex=True)
        df = df.rename(index=str, columns=rename)
        return df

    def to_response(self, file_name, data=None, queryset=None):
        # get data frame
        df = self._create_data_frame(data=data, queryset=queryset)

        # create response
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv', status=200)
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['file-name'] = file_name

        df.to_csv(
            response,
            index=False,
            header=True,
            sep=';',
            float_format='%.2f',
            date_format='%Y-%m-%d %H:%M:%S',
            decimal=',',
            encoding='utf-8'
        )
        return response


class ReleaseNotesBehavior:

    @staticmethod
    def map_release_notes(release: dict) -> dict:
        regex_version = r'Versões:\s+\((.*?)\)\s+\((.*?)\)'
        release_date = datetime.strptime(release.get('released_at').split('T')[0], '%Y-%m-%d')
        if 'project' in release.get('tag_name', '') and release.get('description') and release_date <= datetime.now():
            version_project = re.search(
                regex_version,
                release.get('description').replace('web-', '').replace('api-', '')
            )
            if version_project:
                return {
                    'name': release.get('name'),
                    'version_project': release.get('tag_name').replace('project-', ''),
                    'version_api': version_project.group(1),
                    'version_web': version_project.group(2),
                    'description': release.get('description'),
                    'released_at': release.get('released_at'),
                }

    def get_release_notes(self):
        url = f"https://{os.environ.get('ROUTER_GITLAB')}/api/v4/projects/{os.environ.get('ID_PROJECT')}/releases/"
        headers = {"PRIVATE-TOKEN": os.environ.get('TOKEN_PROJECT')}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise exceptions.ReleaseNotesNotFoundException

        return filter(None, map(self.map_release_notes, response.json()))

    def run(self):
        return self.get_release_notes()
