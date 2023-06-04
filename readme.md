# OSF Recursive Uploader

This Python script provides a way to recursively upload files from a local directory to your project on the Open Science Framework (OSF).

## Why this exists

While OSF is a fantastic platform for sharing scientific data and materials, the web interface doesn't currently provide an option to recursively upload a directory and its subdirectories. This tool fills that gap by providing a CLI for doing just that.

## How to use it

To run the script, you first need to install the required dependencies:

```bash
pip install osfclient
```

Once the dependencies are installed, you can use the script from the command line like this:

```bash
python osf_upload.py -p <project-id> -u <username> -t <token> -s <source-dir> -d <destination-dir> -f -i <ignore-regex>
```

## Parameters

* `-p, --project` (Required): The ID of the OSF project you want to upload to.
* `-u, --username` (Required for private projects): Your OSF username.
* `-t, --token` (Required for private projects): Your OSF token.
* `-pass, --password` (Optional): Your OSF token.
* `-s, --source` (Optional, default=`"."`): The local directory you want to upload.
* `-d, --destination` (Optional, default=`""`): The directory on OSF storage where you want to upload the files.
* `-f, --force` (Optional, default=`False`): If set, this will overwrite files on OSF if they exist.
* `-i, --ignore` (Optional): A regular expression pattern for files or directories to ignore. For example, use `^\.` to ignore ".git" files.

Note: `username` and `token` are required for authenticating with OSF.

## Typical Example

The following uploads the contents of the current directory to the root of a project, ignoring any files or directories that start with a dot:

```bash
python osf_upload.py -p myprojectid -u myusername -t mytoken -i "^\."
```

## Output

The script will print out information about the upload process, including which files are being uploaded and which are being skipped (if any). Upon completion, it will provide a summary of how many files were uploaded, how many were skipped, and how long the upload process took.

```bash
Connecting to OSF project <project>...
Uploading files in directory: .
  - /test/osf_upload.py
  - /test/readme.md
Uploaded 2 file(s), skipped 0 file(s).
Elapsed time: 4.52731204032898 seconds.
```
