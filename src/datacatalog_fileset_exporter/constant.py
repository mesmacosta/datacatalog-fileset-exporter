# Constants used for creating the Filesets.
FILESETS_ENTRY_GROUP_NAME_COLUMN_LABEL = 'entry_group_name'
FILESETS_ENTRY_GROUP_DISPLAY_NAME_COLUMN_LABEL = 'entry_group_display_name'
FILESETS_ENTRY_GROUP_DESCRIPTION_COLUMN_LABEL = 'entry_group_description'
FILESETS_ENTRY_ID_COLUMN_LABEL = 'entry_id'
FILESETS_ENTRY_DISPLAY_NAME_COLUMN_LABEL = 'entry_display_name'
FILESETS_ENTRY_DESCRIPTION_COLUMN_LABEL = 'entry_description'
FILESETS_ENTRY_FILE_PATTERNS_COLUMN_LABEL = 'entry_file_patterns'
FILESETS_ENTRY_SCHEMA_COLUMN_NAME_COLUMN_LABEL = 'schema_column_name'
FILESETS_ENTRY_SCHEMA_COLUMN_TYPE_COLUMN_LABEL = 'schema_column_type'
FILESETS_ENTRY_SCHEMA_COLUMN_DESCRIPTION_COLUMN_LABEL = 'schema_column_description'
FILESETS_ENTRY_SCHEMA_COLUMN_MODE_COLUMN_LABEL = 'schema_column_mode'

# Expected order for the CSV header columns.
FILESETS_COLUMNS_ORDER = (FILESETS_ENTRY_GROUP_NAME_COLUMN_LABEL,
                          FILESETS_ENTRY_GROUP_DISPLAY_NAME_COLUMN_LABEL,
                          FILESETS_ENTRY_GROUP_DESCRIPTION_COLUMN_LABEL,
                          FILESETS_ENTRY_ID_COLUMN_LABEL, FILESETS_ENTRY_DISPLAY_NAME_COLUMN_LABEL,
                          FILESETS_ENTRY_DESCRIPTION_COLUMN_LABEL,
                          FILESETS_ENTRY_FILE_PATTERNS_COLUMN_LABEL,
                          FILESETS_ENTRY_SCHEMA_COLUMN_NAME_COLUMN_LABEL,
                          FILESETS_ENTRY_SCHEMA_COLUMN_TYPE_COLUMN_LABEL,
                          FILESETS_ENTRY_SCHEMA_COLUMN_DESCRIPTION_COLUMN_LABEL,
                          FILESETS_ENTRY_SCHEMA_COLUMN_MODE_COLUMN_LABEL)

# Columns that can be empty and will be automatically filled on the CSV.
FILESETS_FILLABLE_COLUMNS = [
    FILESETS_ENTRY_GROUP_NAME_COLUMN_LABEL, FILESETS_ENTRY_GROUP_DISPLAY_NAME_COLUMN_LABEL,
    FILESETS_ENTRY_GROUP_DESCRIPTION_COLUMN_LABEL
]

# Columns that are required on the CSV.
FILESETS_NON_FILLABLE_COLUMNS = [
    FILESETS_ENTRY_ID_COLUMN_LABEL, FILESETS_ENTRY_DISPLAY_NAME_COLUMN_LABEL,
    FILESETS_ENTRY_DESCRIPTION_COLUMN_LABEL, FILESETS_ENTRY_FILE_PATTERNS_COLUMN_LABEL,
    FILESETS_ENTRY_SCHEMA_COLUMN_NAME_COLUMN_LABEL, FILESETS_ENTRY_SCHEMA_COLUMN_TYPE_COLUMN_LABEL,
    FILESETS_ENTRY_SCHEMA_COLUMN_DESCRIPTION_COLUMN_LABEL,
    FILESETS_ENTRY_SCHEMA_COLUMN_MODE_COLUMN_LABEL
]

# Value used to split the values inside FILESETS_ENTRY_FILE_PATTERNS_COLUMN_LABEL field.
FILE_PATTERNS_VALUES_SEPARATOR = "|"