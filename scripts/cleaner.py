import argparse
import sys
import time

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ACCOUNTS = {
    "dev": "technical.admin@test.tierone.cirruseo.com",
    "preprod": "admin.cirruseo@urbanis.fr",
}

SD_PREFIXES = ["Mission :", "ZZ - [ARCHIVE]"]

GROUP_PREFIXES = ["oslo-mission"]


def start(env, kind, commit=False):
    if kind == "drive":
        start_drive_cleanup(env, commit)
    elif kind == "groups":
        start_groups_cleanup(env, commit)
    else:
        print("Nothing to do.")


def start_groups_cleanup(env, commit=False):
    creds = Credentials.from_service_account_file(
        f"keys/{env}.json",
        scopes=["https://www.googleapis.com/auth/admin.directory.group"],
        subject=ACCOUNTS.get(env),
    )

    service = build("admin", "directory_v1", credentials=creds)

    next_token = None
    while True:
        response = (
            service.groups()
            .list(
                customer="my_customer",
                query=f"email:{env}.oslo-mission*",
                fields="groups(id,email),nextPageToken",
                maxResults=200,
                pageToken=next_token,
            )
            .execute(num_retries=3)
        )

        NEW_GROUP_PREFIXES = [f"{env}.{element}" for element in GROUP_PREFIXES]
        for group in response.get("groups", []):
            if list(filter(group.get("email").startswith, NEW_GROUP_PREFIXES)):
                print(group.get("email"))
                handle_group(group.get("id"), service, commit)
                if commit:
                    time.sleep(2)

        if response.get("nextPageToken"):
            next_token = response.get("nextPageToken")
        else:
            break


def handle_group(group_id, service, commit):
    r = service.groups().delete(groupKey=group_id)
    if commit:
        try:
            r.execute(num_retries=3)
        except HttpError as e:
            print(f"Unable to delete google group {group_id} : {e}")
        else:
            print(f"Google group {group_id} deleted.")
    else:
        print(f"Would have delete google group {group_id}")


def start_drive_cleanup(env, commit=False):
    creds = Credentials.from_service_account_file(
        f"keys/{env}.json",
        scopes=["https://www.googleapis.com/auth/drive"],
        subject=ACCOUNTS.get(env),
    )
    service = build("drive", "v3", credentials=creds)

    next_token = None
    while True:
        response = (
            service.drives()
            .list(
                fields="drives(id,name),nextPageToken",
                pageSize=100,
                pageToken=next_token,
            )
            .execute(num_retries=3)
        )
        NEW_SD_PREFIXES = [f"[{env.upper()}] {element}" for element in SD_PREFIXES]
        for drive in response.get("drives", []):
            if list(filter(drive.get("name").startswith, NEW_SD_PREFIXES)):
                print(drive.get("name"))
                handle_drive(drive.get("id"), service, commit)
        if response.get("nextPageToken"):
            next_token = response.get("nextPageToken")
        else:
            break


def handle_drive(drive_id, service, commit=False):
    next_token = None
    print(f"Handling Shared Drive {drive_id}")
    while True:
        try:
            response = (
                service.files()
                .list(
                    q=f"'{drive_id}' in parents",
                    supportsAllDrives=True,
                    fields="files(id),nextPageToken",
                    includeItemsFromAllDrives=True,
                    pageToken=next_token,
                )
                .execute(num_retries=3)
            )
            has_children = len(response.get("files", [])) > 0
            for item in response.get("files", []):
                delete_item(item.get("id"), service, commit)
            if response.get("nextPageToken"):
                next_token = response.get("nextPageToken")
            else:
                break
        except HttpError as e:
            print(f"Unable to list children of shared drive {drive_id} : {e}")
            break
    print(f"Getting ready to delete shared drive {drive_id}")
    time.sleep(2 if not has_children else 15)
    delete_drive(drive_id, service, commit)


def delete_drive(drive_id, service, commit=False):
    r = service.drives().delete(driveId=drive_id)
    if commit:
        try:
            r.execute(num_retries=3)
        except HttpError as e:
            print(f"Unable to delete shared drive {drive_id} : {e}")
        else:
            print(f"Shared drive {drive_id} deleted.")
    else:
        print(f"Would have delete shared drive {drive_id}")


def delete_item(file_id, service, commit=False):
    r = service.files().delete(fileId=file_id, supportsAllDrives=True)
    if commit:
        r.execute(num_retries=True)
        print(f"File {file_id} deleted.")
    else:
        print(f"Would have delete file {file_id}.")


def cmdline_args():

    # Make parser object
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    p.add_argument(
        "-e",
        "--env",
        type=str,
        choices=["dev", "preprod"],
        default="dev",
        help="environment to clean : dev | preprod",
    )

    p.add_argument(
        "-c",
        "--commit",
        action="store_true",
        help="by default the script will execute as a dry run",
    )

    p.add_argument(
        "-k",
        "--kind",
        type=str,
        choices=["drive", "groups"],
        default="drive",
        help="cleanup kind: drive or google groups",
    )

    return p.parse_args()


if __name__ == "__main__":
    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)

    try:
        args = cmdline_args()
    except:
        sys.exit(1)

    start(args.env, args.kind, args.commit)
