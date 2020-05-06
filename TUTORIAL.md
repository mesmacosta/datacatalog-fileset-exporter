<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-fileset-exporter&tutorial=TUTORIAL.md--->
# Data Catalog Fileset Exporter Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Fileset Exporter Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-fileset-exporter"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Fileset Exporter.

## CLI

Each product's api definition is stored in the magic-modules repo.

Let's open
<walkthrough-editor-open-file filePath="src/datacatalog_fileset_exporter/datacatalog_fileset_exporter_cli.py"
                              text="datacatalog_fileset_exporter_cli.py">
</walkthrough-editor-open-file>.

### CLI Args

The
<walkthrough-editor-select-regex filePath="README.md"
                                 text="top section">
</walkthrough-editor-select-regex>
provides metadata about the API, such as name, scopes, and versions.

## Compiling magic-modules

Now, let's compile those changes.

Since we're running in Cloud Shell, this command will make sure we connect to GitHub via HTTPS
instead of SSH. You will probably not have to do this in your typical development environment.

First, run `bundle install` to make sure all ruby dependencies are available:
```bash
bundle install
```

Then, check out a copy of Ansible's GCP collection to a folder called `build/ansible`.
```bash
git clone https://github.com/ansible-collections/ansible_collections_google.git ./build/ansible
```

Next, run the compiler:
```bash
bundle exec compiler -p products/pubsub -e ansible -o build/ansible
```

This command tells us to run the compiler for the pubsub API, and generate Ansible into the
`build/ansible` directory.

Let's see our changes! Navigate to the Ansible submodule and run `git diff` to see what changed:
```bash
cd build/ansible && git diff
```

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully made a change to a resource in Magic Modules.
