import logging
import re
from functools import lru_cache

from google.api_core import exceptions
from google.cloud import datacatalog


class DataCatalogFacade:
    """Data Catalog API communication facade."""

    __NESTED_LOG_PREFIX = ' ' * 5

    def __init__(self):
        # Initialize the API client.
        self.__datacatalog = datacatalog.DataCatalogClient()

    # Currently we don't have a list method, so we are using search which is not exhaustive,
    # and might not return some entries.
    def search_filesets(self, project_ids, date_created=None):
        scope = datacatalog.types.SearchCatalogRequest.Scope()

        scope.include_project_ids.extend(project_ids.split(','))

        query = 'type=FILESET'

        if date_created:
            query = '{} createtime>{}'.format(query, date_created)

        results_iterator = self.__datacatalog.search_catalog(scope=scope,
                                                             query=query,
                                                             order_by='relevance',
                                                             page_size=1000)

        results = []
        for page in results_iterator.pages:
            results.extend(page)

        return results

    @lru_cache(maxsize=16)
    def get_entry(self, name):
        self.__log_operation_start('GET Entry: %s', name)
        entry = self.__datacatalog.get_entry(name=name)
        self.__log_single_object_read_result(entry)
        return entry

    @lru_cache(maxsize=16)
    def get_entry_group(self, name):
        self.__log_operation_start('GET Entry: %s', name)
        try:
            entry_group = self.__datacatalog.get_entry_group(name=name)
            self.__log_single_object_read_result(entry_group)
            return entry_group
        except exceptions.GoogleAPICallError as e:
            logging.warning('Exception getting Entry Group %s: %s', name, str(e))

    def get_entries_from_search_results(self, search_results):
        entries = []

        for search_result in search_results:
            entry_name = search_result.relative_resource_name
            try:
                entry = self.get_entry(entry_name)
                entries.append(entry)
            except exceptions.GoogleAPICallError as e:
                logging.warning('Exception getting Entry %s: %s', entry_name, str(e))

        return entries

    @classmethod
    def extract_resources_from_entry_name(cls, entry_name):
        re_match = re.match(
            r'^projects[/]([_a-zA-Z-\d]+)[/]locations[/]'
            r'([a-zA-Z-\d]+)[/]entryGroups[/]([@a-zA-Z-_\d]+)'
            r'[/]entries[/]([a-zA-Z-_\d]+)$', entry_name)

        if re_match:
            project_id, location_id, entry_group_id, entry_id, = re_match.groups()
            return project_id, location_id, entry_group_id, entry_id

    @classmethod
    def __log_operation_start(cls, message, *args):
        logging.info('')
        logging.info(message, *args)
        logging.info('--------------------------------------------------')

    @classmethod
    def __log_single_object_read_result(cls, the_object):
        logging.info('%sFound!' if the_object else '%sNOT found!', cls.__NESTED_LOG_PREFIX)
