from typing import List

from flask_sqlalchemy import Pagination
from sqlalchemy import or_

import app.project.requesters.service as requester_service
from app import db
from app.common.exceptions import InconsistentUpdateIdException
from app.project.taxable_incomes import TaxableIncome
from app.project.taxable_incomes.error_handlers import TaxableIncomeNotFoundException
from app.project.taxable_incomes.interface import TaxableIncomeInterface


class TaxableIncomeService:
    @staticmethod
    def create(new_attrs: TaxableIncomeInterface) -> TaxableIncome:
        """Create a new taxable_income with linked requester"""
        requester_service.RequesterService.get_by_id(new_attrs.get("requester_id"))
        taxable_income = TaxableIncome(**new_attrs)
        db.session.add(taxable_income)
        db.session.commit()
        return taxable_income

    @staticmethod
    def create_list(
        new_taxable_incomes: List[TaxableIncomeInterface], requester_id: int
    ) -> List[TaxableIncome]:
        """Create taxable_incomes from a list"""
        taxable_incomes = []
        for taxable_income in new_taxable_incomes:
            taxable_income["requester_id"] = requester_id
            taxable_incomes.append(TaxableIncomeService.create(taxable_income))
        return taxable_incomes

    @staticmethod
    def get_by_id(taxable_income_id: str) -> TaxableIncome:
        db_taxable_income = TaxableIncome.query.get(taxable_income_id)
        if db_taxable_income is None:
            raise TaxableIncomeNotFoundException
        return db_taxable_income

    @staticmethod
    def update(
        taxable_income: TaxableIncome,
        changes: TaxableIncomeInterface,
        force_update: bool = False,
    ) -> TaxableIncome:
        if force_update or TaxableIncomeService.has_changed(taxable_income, changes):
            # If one tries to update entity id, a error must be raised
            if changes.get("id") and changes.get("id") != taxable_income.id:
                raise InconsistentUpdateIdException()
            taxable_income.update(changes)
            db.session.commit()
        return taxable_income

    @staticmethod
    def update_list(list_changes, requester_id: int):

        old_taxable_incomes = TaxableIncome.query.filter_by(
            requester_id=requester_id
        ).all()

        for taxable_income_changes in list_changes:
            # If taxable_income exists, it must be updated
            if "id" in taxable_income_changes:
                taxable_income = TaxableIncomeService.get_by_id(
                    taxable_income_changes["id"]
                )
                TaxableIncomeService.update(taxable_income, taxable_income_changes)
            # Else, it must be created
            else:
                taxable_income_changes["requester_id"] = requester_id
                TaxableIncomeService.create(taxable_income_changes)

        # Compare old taxable_income list and new list and delete obsolete taxable_incomes
        for old_taxable_income in old_taxable_incomes:
            is_removed = True
            for new_taxable_income in list_changes:
                if (
                    "id" in new_taxable_income
                    and new_taxable_income["id"] == old_taxable_income.id
                ):
                    is_removed = False
                    break
            if is_removed:
                TaxableIncomeService.delete_by_id(old_taxable_income.id)

    @staticmethod
    def has_changed(
        taxable_income: TaxableIncome, changes: TaxableIncomeInterface
    ) -> bool:
        for key, value in changes.items():
            if getattr(taxable_income, key) != value:
                return True
        return False

    @staticmethod
    def delete_by_id(taxable_income_id: int) -> int or None:
        taxable_income = TaxableIncome.query.filter(
            TaxableIncome.id == taxable_income_id
        ).first()
        if not taxable_income:
            raise TaxableIncomeNotFoundException
        db.session.delete(taxable_income)
        db.session.commit()
        return taxable_income_id
