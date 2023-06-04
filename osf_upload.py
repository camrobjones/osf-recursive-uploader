"""Recursively upload files to OSF."""

import re
import os
import re
import time
import argparse
from osfclient import OSF

def split_storage(path):
    components = path.split('/')
    if len(components) < 2 or components[0] == '':
        return 'osfstorage', path
    return components[0], '/'.join(components[1:])

def upload_directory(args):
    """
    Upload a directory to OSF.
    
    Parameters
    ----------
    args: Args
        Argument object with project, source, destination, recursive, and force attributes.
    ignore_pattern: str
        A regular expression pattern for files or directories to ignore.
    """
    start_time = time.time()

    # Connect to OSF
    print(f"Connecting to OSF project {args.project}...")
    osf = OSF(username=args.username, password=args.password, token=args.token)

    # Connect to the project
    project = osf.project(args.project)

    # Connect to the storage
    storage, remote_path = split_storage(args.destination)
    store = project.storage()

    # Generate a list of all files currently in the OSF storage
    existing_files = [file_.path for file_ in store.files]

    # Compile the ignore pattern for efficient matching
    ignore_re = re.compile(args.ignore) if args.ignore else None

    # Local name of the directory that is being uploaded
    _, dir_name = os.path.split(args.source.rstrip('/'))

    uploaded_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(args.source):
        # Check if any directories in dirs match the ignore pattern. If they do, remove them from dirs.
        if ignore_re:
            dirs[:] = [d for d in dirs if not ignore_re.match(d)]

        subdir_path = os.path.relpath(root, args.source)

        current_dir = os.path.normpath(os.path.join(dir_name, subdir_path))
        print(f'Uploading files in directory: {current_dir}')
        for fname in files:
            if ignore_re and ignore_re.match(fname):
                skipped_count += 1
                continue

            local_path = os.path.join(root, fname)
            name = os.path.join('/', remote_path, dir_name, subdir_path, fname)
            name = os.path.normpath(name)

            if name not in existing_files or args.force:
                with open(local_path, 'rb') as fp:
                    store.create_file(name, fp, update=args.force)
                    uploaded_count += 1
                    print(f'  - {name}')
            else:
                skipped_count += 1

    print(f'Uploaded {uploaded_count} file(s), skipped {skipped_count} file(s).')
    print(f'Elapsed time: {time.time() - start_time} seconds.')

def main():
    parser = argparse.ArgumentParser(description='Upload files to OSF storage.')
    parser.add_argument('-p', '--project', required=True, help='OSF project id.')
    parser.add_argument('-t', '--token', help='OSF token.')
    parser.add_argument('-u', '--username', help='OSF username.')
    parser.add_argument('-pass', '--password', help='OSF password.')
    parser.add_argument('-s', '--source', default=".", help='Local directory to upload.')
    parser.add_argument('-d', '--destination', help='Remote directory on OSF storage.')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite files on OSF if they exist.')
    parser.add_argument('-i', '--ignore', help='Regular expression pattern for files or directories to ignore.')

    args = parser.parse_args()

    args.destination = f"{args.project}/" if args.destination is None else args.destination 

    upload_directory(args)

if __name__ == "__main__":
    main()

