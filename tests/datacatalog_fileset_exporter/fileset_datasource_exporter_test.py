import os
import unittest
from unittest import mock

import pandas as pd
from google.cloud import datacatalog
from pandas._testing import assert_frame_equal

from datacatalog_fileset_exporter import fileset_datasource_exporter, constant


class FilesetDatasourceExporterTest(unittest.TestCase):

    @mock.patch('datacatalog_fileset_exporter.datacatalog_facade.DataCatalogFacade')
    def setUp(self, mock_datacatalog_facade):
        self.__fileset_datasource_exporter = fileset_datasource_exporter. \
            FilesetDatasourceExporter()
        # Shortcut for the object assigned to self.__datacatalog_facade.__datacatalog
        self.__datacatalog_facade = mock_datacatalog_facade.return_value
        self.__csv_file_path = os.path.dirname(os.path.abspath(__file__))
        self.__filesets_file_path = os.path.join(self.__csv_file_path, 'filesets.csv')

    def test_constructor_should_set_instance_attributes(self):
        self.assertIsNotNone(self.__fileset_datasource_exporter.
                             __dict__['_FilesetDatasourceExporter__datacatalog_facade'])

    def test_export_tag_templates_when_no_templates_should_create_empty_file(self):
        self.__fileset_datasource_exporter.export_filesets('my-project', self.__filesets_file_path)

        created_fileset_file = pd.read_csv(self.__filesets_file_path)

        # Cleans up templates file.
        os.remove(self.__filesets_file_path)

        self.assertTrue(created_fileset_file.empty)

        self.assertEqual(1, self.__datacatalog_facade.search_filesets.call_count)
        self.assertEqual(1, self.__datacatalog_facade.get_entries_from_search_results.call_count)

    def test_export_tag_templates_when_templates_should_create_file(self):
        entry_id = 'my_entry'
        entry_id_2 = 'my_entry_2'

        search_entry_result = MockedObject()
        search_entry_result.relative_resource_name = entry_id
        search_entry_result_2 = MockedObject()
        search_entry_result_2.relative_resource_name = entry_id_2
        self.__datacatalog_facade.search_filesets.return_value = [
            search_entry_result, search_entry_result_2
        ]

        self.__datacatalog_facade.get_entries_from_search_results.return_value = [
            create_default_fileset(entry_id),
            create_default_fileset(entry_id_2)
        ]

        self.__datacatalog_facade.get_entry_group.side_effect = [
            create_default_entry_group('my-entry-group'),
            create_default_entry_group('my-entry-group-2')
        ]

        self.__datacatalog_facade.extract_resources_from_entry_name.return_value = (
            'my-project', 'my-location', 'my-entry-group-id', 'my-entry')

        self.__fileset_datasource_exporter.export_filesets('my-project', self.__filesets_file_path)

        created_fileset_file = pd.read_csv(self.__filesets_file_path)
        expected_fileset_file = pd.read_csv(
            os.path.join(self.__csv_file_path, 'data', 'filesets.csv'))

        # Cleans up fileset file.
        os.remove(self.__filesets_file_path)

        # Fill null fields so the sorting will produce deterministic results.
        created_fileset_file[constant.FILESETS_COLUMNS_ORDER[0]].fillna(method='pad', inplace=True)
        created_fileset_file[constant.FILESETS_COLUMNS_ORDER[1]].fillna(method='pad', inplace=True)
        created_fileset_file[constant.FILESETS_COLUMNS_ORDER[2]].fillna(method='pad', inplace=True)
        expected_fileset_file[constant.FILESETS_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                         inplace=True)
        expected_fileset_file[constant.FILESETS_COLUMNS_ORDER[1]].fillna(method='pad',
                                                                         inplace=True)
        expected_fileset_file[constant.FILESETS_COLUMNS_ORDER[2]].fillna(method='pad',
                                                                         inplace=True)

        self.assertEqual(1, self.__datacatalog_facade.search_filesets.call_count)
        self.assertEqual(1, self.__datacatalog_facade.get_entries_from_search_results.call_count)

        assert_frame_equal(
            created_fileset_file.sort_values([
                constant.FILESETS_COLUMNS_ORDER[0], constant.FILESETS_COLUMNS_ORDER[3],
                constant.FILESETS_COLUMNS_ORDER[7]
            ]),
            expected_fileset_file.sort_values([
                constant.FILESETS_COLUMNS_ORDER[0], constant.FILESETS_COLUMNS_ORDER[3],
                constant.FILESETS_COLUMNS_ORDER[7]
            ]))


def create_default_fileset(entry_name):
    entry = datacatalog.types.Entry()
    entry.name = 'projects/my-project/locations/us-central1/entryGroups/my-entry-group' \
                 '/entries/{}'.format(entry_name)
    entry.display_name = 'My filset'
    entry.description = 'This fileset consists of all files for the bucket'
    entry.gcs_fileset_spec.file_patterns.append('gs://bucket_13c4/*')
    entry.type = datacatalog.enums.EntryType.FILESET

    columns = [
        datacatalog.types.ColumnSchema(column='first_name',
                                       description='First name',
                                       mode='REQUIRED',
                                       type='STRING'),
        datacatalog.types.ColumnSchema(column='first_NAME',
                                       description='First name',
                                       mode='REQUIRED',
                                       type='STRING'),
        datacatalog.types.ColumnSchema(column='last_name',
                                       description='Last name',
                                       mode='REQUIRED',
                                       type='STRING')
    ]

    entry.schema.columns.extend(columns)

    return entry


def create_default_entry_group(entry_group_name):
    entry_group = datacatalog.types.EntryGroup()
    entry_group.name = entry_group_name
    entry_group.display_name = 'My Fileset Entry Group'
    entry_group.description = 'This Entry Group consists of ....'

    return entry_group


class MockedObject(object):

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
