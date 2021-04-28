from .model import TaxableIncome

from flask_restx import Namespace

from .schema import TaxableIncomeSchema

api = Namespace("Taxable_Incomes", description="Taxables incomes namespace")
