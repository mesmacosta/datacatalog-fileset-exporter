import argparse
import logging
import sys

from datacatalog_fileset_exporter import fileset_datasource_exporter


class DatacatalogFilesetExporterCLI:

    @classmethod
    def run(cls, argv):
        cls.__setup_logging()

        args = cls._parse_args(argv)
        args.func(args)

    @classmethod
    def __setup_logging(cls):
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def _parse_args(cls, argv):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        subparsers = parser.add_subparsers()

        cls.add_filesets_cmd(subparsers)

        return parser.parse_args(argv)

    @classmethod
    def add_filesets_cmd(cls, subparsers):
        filesets_parser = subparsers.add_parser("filesets", help="Filesets commands")

        filesets_subparsers = filesets_parser.add_subparsers()

        cls.add_export_filesets_cmd(filesets_subparsers)

    @classmethod
    def add_export_filesets_cmd(cls, subparsers):
        export_filesets_parser = subparsers.add_parser('export', help='Export Filesets to CSV')
        export_filesets_parser.add_argument('--file-path',
                                            help='File path where file will be exported')
        export_filesets_parser.add_argument('--project-ids',
                                            help='Project ids to narrow down Filesets list,'
                                            'split by comma',
                                            required=True)
        export_filesets_parser.add_argument('--date-created',
                                            help='Look for Filesets created after the date, '
                                            'format:YYYY-MM-DDThh:mm:ss.'
                                            ' All timestamps must be in GMT')
        export_filesets_parser.set_defaults(func=cls.__export_filesets)

    @classmethod
    def __export_filesets(cls, args):
        fileset_datasource_exporter.FilesetDatasourceExporter().export_filesets(
            project_ids=args.project_ids, file_path=args.file_path, date_created=args.date_created)


def main():
    argv = sys.argv
    DatacatalogFilesetExporterCLI.run(argv[1:] if len(argv) > 0 else argv)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
