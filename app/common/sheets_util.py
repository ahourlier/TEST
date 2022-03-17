import logging
import os
from typing import List

from googleapiclient.errors import HttpError

from app.common.google_apis import SheetsService


class SheetsUtils:
    @staticmethod
    def get_spreadsheet(
        spreasheet_id,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
        fetch_data=True,
    ):
        """Get a spreadsheets"""
        if not client:
            client = SheetsService(user_email).get()
        try:
            resp = (
                client.spreadsheets()
                .get(spreadsheetId=spreasheet_id, includeGridData=fetch_data)
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            logging.error(f"Unable to get file {spreasheet_id}: {e}")
            return None

    @staticmethod
    def get_spreadsheet_by_datafilter(
        spreasheet_id,
        A1_notation_filters: List = [],
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
        fetch_data=True,
    ):
        """Get a spreadsheets"""
        if not client:
            client = SheetsService(user_email).get()

        data_filters = []
        for filter in A1_notation_filters:
            data_filters.append({"a1Range": filter})

        payload = {"dataFilters": data_filters, "includeGridData": fetch_data}
        try:
            resp = (
                client.spreadsheets()
                .getByDataFilter(spreadsheetId=spreasheet_id, body=payload)
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            logging.error(f"Unable to get file {spreasheet_id}: {e}")
            return None

    @staticmethod
    def format_sheet(sheets_raw_file):
        """Extract and format data from a raw spreadsheets to a more redeable object such as :
        {
        "sheet_name": [
                [value1, value2 etc.]
                [value1, value2 etc.]
                etc.
                ]
        ,
        etc.
        }
        """

        sheet_formatted_values = {}
        for sheet in sheets_raw_file.get("sheets"):
            sheet_formatted_values[
                sheet.get("properties").get("title")
            ] = SheetsUtils.extract_values_from_sheet_rows(
                sheet.get("data")[0].get("rowData")
            )
        return sheet_formatted_values

    @staticmethod
    def extract_values_from_sheet_rows(rows):
        """From a given rows_data, (at Google API format), return a simple list of values
        for each row"""
        rows_data = []
        for row in rows:
            row_data = []
            row_is_empty = True
            for value in row.get("values"):
                effective_value = value.get("effectiveValue")
                if effective_value:
                    row_is_empty = False
                    row_data.append(effective_value.get(next(iter(effective_value))))
                else:
                    row_data.append(None)
            if not row_is_empty:
                rows_data.append(row_data)
            else:
                return rows_data
        return rows_data

    @staticmethod
    def batch_update_spreadsheet(
        spreadsheet_id,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
        client=None,
        changes_map={},
    ):
        """Update a spreadsheet"""
        if not client:
            client = SheetsService(user_email).get()

        requests = []
        for key in changes_map:
            replacement_request = {
                "findReplace": {
                    "find": key,
                    "replacement": changes_map[key],
                    "matchCase": True,
                    "allSheets": True,
                }
            }
            requests.append(replacement_request)

        payload = {"requests": requests}
        try:
            resp = (
                client.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=payload)
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            logging.error(f"Unable to update file {spreadsheet_id}: {e}")
            return None

    @staticmethod
    def create_sheet(payload, user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL")):
        """Create a spreadsheet"""
        client = SheetsService(user_email).get()

        try:
            resp = client.spreadsheets().create(body=payload).execute(num_retries=3)
            return resp
        except HttpError as e:
            logging.error(f"Unable to create spreadsheet with payload {payload}")
            logging.error(f"{e}")
            return None

    @staticmethod
    def add_values(
        sheet_id,
        range,
        array_values,
        client=None,
        user_email=os.getenv("TECHNICAL_ACCOUNT_EMAIL"),
    ):
        """Concat values to a spreadsheet"""
        if not client:
            client = SheetsService(user_email).get()

        try:
            resp = (
                client.spreadsheets()
                .values()
                .append(
                    spreadsheetId=sheet_id,
                    range=range,
                    body={"values": array_values},
                    valueInputOption="RAW",
                )
                .execute(num_retries=3)
            )
            return resp
        except HttpError as e:
            logging.error(f"Unable to add values to spreadsheet {sheet_id}")
            logging.error(array_values)
            logging.error(f"{e}")
            return None
