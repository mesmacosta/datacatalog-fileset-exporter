import unittest
from unittest import mock

import datacatalog_fileset_exporter
from datacatalog_fileset_exporter import datacatalog_fileset_exporter_cli


class DatacatalogFilesetExporterCLITest(unittest.TestCase):

    def test_parse_args_invalid_subcommand_should_raise_system_exit(self):
        self.assertRaises(
            SystemExit, datacatalog_fileset_exporter_cli.DatacatalogFilesetExporterCLI._parse_args,
            ['invalid-subcommand'])

    def test_parse_args_create_tags_missing_mandatory_args_should_raise_system_exit(self):
        self.assertRaises(
            SystemExit, datacatalog_fileset_exporter_cli.DatacatalogFilesetExporterCLI._parse_args,
            ['filesets', 'export'])

    def test_run_no_args_should_raise_attribute_error(self):
        self.assertRaises(AttributeError,
                          datacatalog_fileset_exporter_cli.DatacatalogFilesetExporterCLI.run, None)

    @mock.patch('datacatalog_fileset_exporter.datacatalog_fileset_exporter_cli.'
                'fileset_datasource_exporter.'
                'FilesetDatasourceExporter')
    def test_run_export_tag_templates_should_call_correct_method(
            self, mock_fileset_datasource_exporter):  # noqa: E125

        datacatalog_fileset_exporter_cli.DatacatalogFilesetExporterCLI.run([
            'filesets', 'export', '--file-path', 'test.csv', '--project-ids',
            'my-project1,my-project2'
        ])

        fileset_datasource_processor = mock_fileset_datasource_exporter.return_value
        fileset_datasource_processor.export_filesets.assert_called_once()
        fileset_datasource_processor.export_filesets.assert_called_with(
            date_created=None, project_ids='my-project1,my-project2', file_path='test.csv')

    @mock.patch('datacatalog_fileset_exporter.datacatalog_fileset_exporter_cli.'
                'DatacatalogFilesetExporterCLI')
    def test_main_should_call_cli_run(self, mock_cli):
        datacatalog_fileset_exporter.main()
        mock_cli.run.assert_called_once()
