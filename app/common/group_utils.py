import logging
import os

from googleapiclient.errors import HttpError

from app.common.google_apis import DirectoryService, GroupsSettingsService


class GroupUtils:
    @staticmethod
    def create_google_group(
        email, name, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """Creates a Google Group"""
        if not client:
            client = DirectoryService(user_email).get()
        try:
            payload = {
                "email": email,
                "name": name,
            }
            resp = client.groups().insert(body=payload).execute(num_retries=3)
            return resp.get("id")
        except HttpError as e:
            logging.error(f"Unable to create google group with email {email}: {e}")
            return None

    @staticmethod
    def get_google_group(
        email, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """Gets a Google Group"""
        if not client:
            client = DirectoryService(user_email).get()
        try:
            resp = client.groups().get(groupKey=email).execute(num_retries=3)
            return resp.get("id")
        except HttpError as e:
            logging.warning(f"Unable to get google group with email {email}: {e}")
            return None

    @staticmethod
    def add_member(
        member_email,
        group,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
    ):
        """
        Add a member to a google group
        :param member_email:  email of a member (user or group)
        :param group: either email or google id of a group
        """
        if not client:
            client = DirectoryService(user_email).get()

        try:
            resp = (
                client.members()
                .insert(groupKey=group, body=dict(role="MEMBER", email=member_email))
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            if e.resp.status == 409:
                logging.info(f"Member {member_email} already in group {group}")
                return True
            logging.error(
                f"Unable to add {member_email} as member of group {group}: {e}"
            )
            return None

    @staticmethod
    def remove_member(
        member_email,
        group,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
    ):
        """
        Remove a member from a google group
        :param member_email:  email of a member (user or group)
        :param group: either email or google id of a group
        """
        if not client:
            client = DirectoryService(user_email).get()

        try:
            (
                client.members()
                .delete(groupKey=group, memberKey=member_email)
                .execute(num_retries=3)
            )
            return True
        except HttpError as e:
            logging.error(
                f"Unable to remove {member_email} as member of group {group}: {e}"
            )
            return None

    @staticmethod
    def is_member_of(
        member, group, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """
        Checks whether a user is member of a google group
        :param member: either email or google id of a member (user or group)
        :param group: either email or google id of a group
        :return: True if user is member, else False
        """
        if not client:
            client = DirectoryService(user_email).get()

        try:
            resp = (
                client.members()
                .hasMember(groupKey=group, memberKey=member)
                .execute(num_retries=3)
            )
            return resp.get("isMember", False)
        except HttpError as e:
            logging.error(
                f"Unable to check whether {member} is member of group {group}: {e}"
            )
            return False

    @staticmethod
    def list_members(
        group, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None,
    ):
        """
        List direct members of a group
        :param group: either email or google id of a group
        :return: List of members objects
        """
        if not client:
            client = DirectoryService(user_email).get()

        try:
            resp = (
                client.members()
                .list(groupKey=group, maxResults=200, fields="members(id,email,type)")
                .execute(num_retries=3)
            )
            return resp.get("members", [])
        except HttpError as e:
            logging.error(f"Unable to retrieve members from group {group}: {e}")
            return None

    @staticmethod
    def set_group_visibility_private(
        group_email, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"), client=None
    ):
        """
        Set a group visibility to members only so it does not show up in Directory
        :param group_email: email of the group to update
        :param user_email: email of the user performing the action
        :param client: Groups client
        :return: True if operation is successful
        """
        if not client:
            client = GroupsSettingsService(user_email).get()

        try:
            client.groups().patch(
                groupUniqueId=group_email,
                body=dict(
                    whoCanDiscoverGroup="ALL_MEMBERS_CAN_DISCOVER",
                    whoCanLeaveGroup="NONE_CAN_LEAVE",
                ),
            ).execute(num_retries=3)

            return True
        except HttpError as e:
            logging.error(f"Unable to change group {group_email} visibility: {e}")
            return False
