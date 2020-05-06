<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-fileset-exporter&tutorial=TUTORIAL.md--->
# Data Catalog Fileset Exporter Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Fileset Exporter Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-fileset-exporter"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Fileset Exporter.

## CLI

This script is a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="datacatalog-fileset-exporter/src/datacatalog_fileset_exporter/datacatalog_fileset_exporter_cli.py"
                              text="datacatalog-fileset-exporter/src/datacatalog_fileset_exporter/datacatalog_fileset_exporter_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

## CSV fields

Go to the
<walkthrough-editor-open-file filePath="datacatalog-fileset-exporter/README.md" text="README.md">
</walkthrough-editor-open-file> file, and find the ## 5. Export Filesets to CSV file section.
This section explains the CSV columns created when the CLI is executed.

## Executing the CLI

First, let's set up the Service Account.

```bash
# Get the current project_id
expor PROJECT_ID=$(gcloud config get-value project)

# Create Service Account
gcloud iam service-accounts create datacatalog-fileset-exporter-sa \
--display-name  "Service Account for Fileset Exporter" \
--project $PROJECT_ID

# Create a credentials folder
mkdir -p ~/credentials

# Create and download the Key
gcloud iam service-accounts keys create "~/credentials/datacatalog-fileset-exporter-sa.json" \
--iam-account "datacatalog-fileset-exporter-sa@$PROJECT_ID.iam.gserviceaccount.com"

# Add Data Catalog admin role
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-fileset-exporter-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"

# Set up the credentials
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-fileset-exporter-sa.json
```

Then, install and config the datacatalog-fileset-exporter CLI.
```bash
# Install datacatalog-fileset-exporter
pip3 install datacatalog-fileset-exporter --user

# Set it to your PATH
export PATH=~/.local/bin:$PATH

# Test it out
datacatalog-fileset-exporter --help
```

Next, run the CLI:
```bash
# Create a output folder
mkdir -p ~/output

# Run the CLI
datacatalog-fileset-exporter filesets export --project-ids $PROJECT_ID --file-path ~/output/filesets.csv
```

Let's see the output! Navigate to the Ansible submodule and run `git diff` to see what changed:
```bash
# See if the file was created.
cat ~/output/filesets.csv
```
Use the Cloud Editor to see the results, or upload the CSV to Google Sheets to better visualize it.

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Fileset Exporter Tutorial.
