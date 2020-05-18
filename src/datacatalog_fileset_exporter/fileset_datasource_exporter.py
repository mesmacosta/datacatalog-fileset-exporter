import logging
import os

import pandas as pd
from google.cloud import datacatalog

from . import constant, datacatalog_facade


class FilesetDatasourceExporter:

    def __init__(self):
        self.__datacatalog_facade = datacatalog_facade.DataCatalogFacade()

    def export_filesets(self, project_ids, file_path=None, date_created=None):
        """
        Export Filesets found by searching Data Catalog.

        :param file_path: File path to be exported to.
        :param project_ids: Project ids to narrow down search results.
        :param date_created: Fileset Creation Date.
        """
        logging.info('')
        logging.info('===> Export Filesets [STARTED]')

        if date_created:
            logging.info('=> Looking for Filesets created after: %s', date_created)

        logging.info('')
        logging.info('Exporting the Filesets...')
        self.__export_filesets(project_ids, file_path, date_created)

        logging.info('')
        logging.info('==== Export Filesets [FINISHED] =============')

    def __export_filesets(self, project_ids, file_path=None, date_created=None):
        search_results = self.__datacatalog_facade.search_filesets(project_ids, date_created)
        entries = self.__datacatalog_facade.get_entries_from_search_results(search_results)
        dataframe = self.__entries_to_dataframe(entries)

        if file_path is None:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filesets.csv')

        dataframe.to_csv(file_path, index=False)
        logging.info('Check the generated file at: %s', file_path)

    def __entries_to_dataframe(self, entries):
        dataframe = pd.DataFrame(columns=constant.FILESETS_COLUMNS_ORDER)

        for entry in entries:
            entry_name = entry.name
            entry_display_name = entry.display_name
            entry_description = entry.description

            file_patterns = constant.FILE_PATTERNS_VALUES_SEPARATOR.join(
                [file_pattern for file_pattern in entry.gcs_fileset_spec.file_patterns])

            project_id, location_id, entry_group_id, entry_id = \
                self.__datacatalog_facade.extract_resources_from_entry_name(entry_name)

            entry_group_name = datacatalog.DataCatalogClient.entry_group_path(
                project_id, location_id, entry_group_id)

            entry_group = self.__datacatalog_facade.get_entry_group(entry_group_name)
            if entry_group:
                entry_group_name = entry_group.name
                entry_group_display_name = entry_group.display_name
                entry_group_description = entry_group.description
            else:
                entry_group_name = entry_group_name

            columns = entry.schema.columns

            if len(columns) > 0:
                for column in columns:
                    schema_column_name = column.column
                    schema_column_type = column.type
                    schema_column_description = column.description
                    schema_column_mode = column.mode

                    column_index = list(columns).index(column)

                    if column_index == 0:
                        dataframe = self.__append_values(
                            dataframe, entry_description, entry_display_name,
                            entry_group_description, entry_group_display_name, entry_group_name,
                            entry_id, file_patterns, schema_column_description, schema_column_mode,
                            schema_column_name, schema_column_type)
                    else:
                        dataframe = self.__append_values(dataframe, entry_description,
                                                         entry_display_name, '', '', '', entry_id,
                                                         file_patterns, schema_column_description,
                                                         schema_column_mode, schema_column_name,
                                                         schema_column_type)
            else:
                dataframe = self.__append_values(dataframe, entry_description, entry_display_name,
                                                 entry_group_description, entry_group_display_name,
                                                 entry_group_name, entry_id, file_patterns, '', '',
                                                 '', '')

        return dataframe

    @classmethod
    def __append_values(cls, dataframe, entry_description, entry_display_name,
                        entry_group_description, entry_group_display_name, entry_group_name,
                        entry_id, file_patterns, schema_column_description, schema_column_mode,
                        schema_column_name, schema_column_type):
        dataframe = dataframe.append(
            {
                constant.FILESETS_COLUMNS_ORDER[0]: entry_group_name,
                constant.FILESETS_COLUMNS_ORDER[1]: entry_group_display_name,
                constant.FILESETS_COLUMNS_ORDER[2]: entry_group_description,
                constant.FILESETS_COLUMNS_ORDER[3]: entry_id,
                constant.FILESETS_COLUMNS_ORDER[4]: entry_display_name,
                constant.FILESETS_COLUMNS_ORDER[5]: entry_description,
                constant.FILESETS_COLUMNS_ORDER[6]: file_patterns,
                constant.FILESETS_COLUMNS_ORDER[7]: schema_column_name,
                constant.FILESETS_COLUMNS_ORDER[8]: schema_column_type,
                constant.FILESETS_COLUMNS_ORDER[9]: schema_column_description,
                constant.FILESETS_COLUMNS_ORDER[10]: schema_column_mode
            },
            ignore_index=True)
        return dataframe
