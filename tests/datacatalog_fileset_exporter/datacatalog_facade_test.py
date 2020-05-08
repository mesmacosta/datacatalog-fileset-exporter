import unittest
from unittest import mock

from google.api_core import exceptions

from datacatalog_fileset_exporter import datacatalog_facade


class DataCatalogFacadeTest(unittest.TestCase):

    @mock.patch('datacatalog_fileset_exporter.datacatalog_facade.' 'datacatalog.DataCatalogClient')
    def setUp(self, mock_datacatalog_client):
        self.__datacatalog_facade = datacatalog_facade.DataCatalogFacade()
        # Shortcut for the object assigned to self.__datacatalog_facade.__datacatalog
        self.__datacatalog_client = mock_datacatalog_client.return_value

    def test_constructor_should_set_instance_attributes(self):
        self.assertIsNotNone(self.__datacatalog_facade.__dict__['_DataCatalogFacade__datacatalog'])

    def test_get_entry_should_call_client_library_method(self):
        self.__datacatalog_facade.get_entry(None)

        datacatalog = self.__datacatalog_client
        datacatalog.get_entry.assert_called_once()

    def test_get_entry_group_should_call_client_library_method(self):
        self.__datacatalog_facade.get_entry_group(None)

        datacatalog = self.__datacatalog_client
        datacatalog.get_entry_group.assert_called_once()

    def test_search_filesets_should_return_values(self):
        result_iterator = MockedObject()

        entry = MockedObject()
        entry.name = 'template_1'

        entry_2 = MockedObject()
        entry_2.name = 'template_2'

        expected_return_value = [entry, entry_2]

        # simulates two pages
        result_iterator.pages = [[entry], [entry_2]]

        datacatalog = self.__datacatalog_client
        datacatalog.search_catalog.return_value = result_iterator

        return_value = self.__datacatalog_facade.search_filesets('my-project1,my-project2')

        self.assertEqual(1, datacatalog.search_catalog.call_count)
        self.assertEqual(expected_return_value, return_value)

    def test_search_filesets_with_date_created_should_return_values(self):
        result_iterator = MockedObject()

        entry = MockedObject()
        entry.name = 'template_1'

        entry_2 = MockedObject()
        entry_2.name = 'template_2'

        expected_return_value = [entry, entry_2]

        # simulates two pages
        result_iterator.pages = [[entry], [entry_2]]

        datacatalog = self.__datacatalog_client
        datacatalog.search_catalog.return_value = result_iterator

        return_value = self.__datacatalog_facade.search_filesets('my-project1,my-project2',
                                                                 '2020-01-01')

        self.assertEqual(1, datacatalog.search_catalog.call_count)
        self.assertEqual(expected_return_value, return_value)

    def test_get_entries_from_search_results_should_return_values(self):
        entry = MockedObject()
        entry.name = 'asset_1'
        entry.relative_resource_name = 'asset_1_resource_name'

        entry_2 = MockedObject()
        entry_2.name = 'asset_2'
        entry_2.relative_resource_name = 'asset_2_resource_name'

        search_results = [entry, entry_2]

        datacatalog = self.__datacatalog_client
        datacatalog.get_tag_template.return_value = {}

        self.__datacatalog_facade.get_entries_from_search_results(search_results)

        self.assertEqual(2, datacatalog.get_entry.call_count)

    def test_get_entries_err_from_search_results_should_return_values(self):
        entry = MockedObject()
        entry.name = 'asset_1'
        entry.relative_resource_name = 'asset_1_resource_name'

        entry_2 = MockedObject()
        entry_2.name = 'asset_2'
        entry_2.relative_resource_name = 'asset_2_resource_name'

        search_results = [entry, entry_2]

        datacatalog = self.__datacatalog_client
        datacatalog.get_entry.side_effect = [{},
                                             exceptions.GoogleAPICallError('Permission denied')]

        self.__datacatalog_facade.get_entries_from_search_results(search_results)

        self.assertEqual(2, datacatalog.get_entry.call_count)

    def test_extract_resources_from_entry_should_return_values(self):
        resource_name = 'projects/my-project/locations/us-central1/entryGroups/my-entry-group' \
                        '/entries/my_entry'

        project_id, location_id, entry_group_id, entry_id = \
            self.__datacatalog_facade.extract_resources_from_entry_name(resource_name)

        self.assertEqual('my-project', project_id)
        self.assertEqual('us-central1', location_id)
        self.assertEqual('my-entry-group', entry_group_id)
        self.assertEqual('my_entry', entry_id)


class MockedObject(object):

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
