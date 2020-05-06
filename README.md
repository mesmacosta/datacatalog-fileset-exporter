# Datacatalog Fileset Exporter

[![CircleCI][1]][2] [![PyPi][7]][8] [![License][9]][9] [![Issues][10]][11]

A Python package to manage Google Cloud Data Catalog Fileset export scripts.

**Disclaimer: This is not an officially supported Google product.**

## Executing in Cloud Shell
````bash
# Set your SERVICE ACCOUNT, for instructions go to 1.3. Auth credentials
# This name is just a suggestion, feel free to name it following your naming conventions
export GOOGLE_APPLICATION_CREDENTIALS=~/datacatalog-fileset-exporter-sa.json

# Install datacatalog-fileset-exporter
pip3 install datacatalog-fileset-exporter --user

# Add to your PATH
export PATH=~/.local/bin:$PATH

# Look for available commands
datacatalog-fileset-exporter --help
````

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-fileset-exporter&tutorial=TUTORIAL.md)

## 1. Environment setup

### 1.1. Python + virtualenv

Using [virtualenv][3] is optional, but strongly recommended unless you use [Docker](#12-docker).

#### 1.1.1. Install Python 3.6+

#### 1.1.2. Get the source code
```bash
git clone https://github.com/mesmacosta/datacatalog-fileset-exporter
cd ./datacatalog-fileset-exporter
```

_All paths starting with `./` in the next steps are relative to the `datacatalog-fileset-exporter`
folder._

#### 1.1.3. Create and activate an isolated Python environment

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

#### 1.1.4. Install the package

```bash
pip install --upgrade .
```

### 1.2. Docker

Docker may be used as an alternative to run the script. In this case, please disregard the
[Virtualenv](#11-python--virtualenv) setup instructions.

### 1.3. Auth credentials

#### 1.3.1. Create a service account and grant it below roles

- Data Catalog Admin

#### 1.3.2. Download a JSON key and save it as
This name is just a suggestion, feel free to name it following your naming conventions
- `./credentials/datacatalog-fileset-exporter-sa.json`

#### 1.3.3. Set the environment variables

_This step may be skipped if you're using [Docker](#12-docker)._

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-fileset-exporter-sa.json
```

## 5. Export Filesets to CSV file

### 5.1. A CSV file representing the Filesets will be created

Filesets are composed of as many lines as required to represent all of their fields. The columns are
described as follows:

| Column                        | Description               | Mandatory |
| ---                           | ---                       | ---       |
| **entry_group_name**          | Entry Group Name.         | Y         |
| **entry_group_display_name**  | Entry Group Display Name. | Y         |
| **entry_group_description**   | Entry Group Description.  | Y         |
| **entry_id**                  | Entry ID.                 | Y         |
| **entry_display_name**        | Entry Display Name.       | Y         |
| **entry_description**         | Entry Description.        | Y         |
| **entry_file_patterns**       | Entry File Patterns.      | Y         |
| **schema_column_name**        | Schema column name.       | N         |
| **schema_column_type**        | Schema column type.       | N         |
| **schema_column_description** | Schema column description.| N         |
| **schema_column_mode**        | Schema column mode.       | N         |

### 5.2. Run the datacatalog-fileset-exporter script

- Python + virtualenv

```bash
datacatalog-fileset-exporter filesets export --project-ids my-project --file-path CSV_FILE_PATH
```


[1]: https://circleci.com/gh/mesmacosta/datacatalog-fileset-exporter.svg?style=svg
[2]: https://circleci.com/gh/mesmacosta/datacatalog-fileset-exporter
[3]: https://virtualenv.pypa.io/en/latest/
[7]: https://img.shields.io/pypi/v/datacatalog-fileset-exporter.svg?force_cache=true
[8]: https://pypi.org/project/datacatalog-fileset-exporter/
[9]: https://img.shields.io/github/license/mesmacosta/datacatalog-fileset-exporter.svg
[10]: https://img.shields.io/github/issues/mesmacosta/datacatalog-fileset-exporter.svg
[11]: https://github.com/mesmacosta/datacatalog-fileset-exporter/issues
