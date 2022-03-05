# Allow import from siblings directory
import sys
import os
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

import functools
from app import create_app, db
from simulation_calculations.csv_utils import *
from simulation_calculations.calcul import *

app = create_app("dev")

DRY_RUN = True

def handle_pb(project):
    from app.project.simulations.model import SimulationSubResult
    from app.project.accommodations import Accommodation
    from app.project.quotes.model import QuoteAccommodation

    simulations = project.simulations
    if len(simulations) == 0:
        return

    for s in simulations:
        if needs_calculation(s):
            sub_results = {}
            for sa in s.simulations_accommodations:
                sub_results[sa.accommodation_id] = {
                    "price_incl_tax": 0,
                    "total_subvention": 0,
                    "remaining_cost": 0,
                    "subvention_on_ttc": 0,
                }
            sub_results["common_area"] = {
                "id": project.common_areas.id,
                "price_incl_tax": 0,
                "total_subvention": 0,
                "remaining_cost": 0,
                "subvention_on_ttc": 0,
            }
            for quote in s.quotes:
                sub_results["common_area"]["price_incl_tax"] += (
                    quote.price_incl_tax if quote.price_incl_tax else 0
                )
                for quote_accommodation in quote.accommodations:
                    sub_results[quote_accommodation["accommodation"].id][
                        "price_incl_tax"
                    ] += quote_accommodation["price_incl_tax"]
            for sf in s.simulation_funders:
                if len(sf.funder_accommodations) > 0:
                    for fa in sf.funder_accommodations:
                        if subvention_needs_calculation(fa):
                            fa.subvention = calculate_subvention(fa)
                        if fa.is_common_area:
                            sub_results["common_area"]["total_subvention"] += (
                                fa.subvention if fa.subvention is not None else 0
                            )
                        else:
                            sub_results[fa.accommodation_id]["total_subvention"] += (
                                fa.subvention if fa.subvention is not None else 0
                            )
                else:
                    pass

            for accommodation in sub_results:
                sub_results[accommodation]["remaining_cost"] = sub_results[
                    accommodation
                ].get("price_incl_tax", 0) - sub_results[accommodation].get(
                    "total_subvention", 0
                )
                sub_results[accommodation]["subvention_on_ttc"] = round(
                    (
                        (
                            sub_results[accommodation].get("price_incl_tax", 0)
                            - sub_results[accommodation]["remaining_cost"]
                        )
                        / sub_results[accommodation].get("price_incl_tax", 1)
                    )
                    * 100,
                    0,
                ) if sub_results[accommodation].get("price_incl_tax", 0) != 0 else 0

            write_log_in_csv(
                [
                    project.id,
                    s.name,
                    functools.reduce(
                        lambda a, b: a + b,
                        [s.get("price_incl_tax") for s in sub_results.values()],
                    ),
                    functools.reduce(
                        lambda a, b: a + b,
                        [s.get("total_subvention") for s in sub_results.values()],
                    ),
                    functools.reduce(
                        lambda a, b: a + b,
                        [s.get("remaining_cost") for s in sub_results.values()],
                    ),
                    functools.reduce(
                        lambda a, b: a + b,
                        [s.get("subvention_on_ttc") for s in sub_results.values()],
                    ),
                    "",
                ]
            )

def handle_po_tenant_sdc(project):
    simulations = project.simulations
    if len(simulations) == 0:
        return

    for s in simulations:
        if needs_calculation(s):
            total_price_incl_tax = 0
            total_subventions = 0
            total_advances = 0
            total_price_incl_tax = get_total_price_incl_tax(s)
            for sf in s.simulation_funders:

                sf.subvention = calculate_subvention(sf)

                total_subventions += sf.subvention if sf.subvention else 0
                total_advances += sf.advance if sf.advance else 0
            remaining_cost = total_price_incl_tax - total_subventions
            subvention_on_ttc = round(
                ((total_price_incl_tax - remaining_cost) / total_price_incl_tax) * 100,
                0,
            )
            write_log_in_csv(
                [
                    project.id,
                    s.name,
                    total_price_incl_tax,
                    total_subventions,
                    remaining_cost,
                    subvention_on_ttc,
                    total_advances,
                ]
            )
            if not DRY_RUN:
                s.total_work_price = total_price_incl_tax
                s.total_subventions = total_subventions
                s.remaining_costs = remaining_cost
                s.subvention_on_TTC = subvention_on_ttc
                s.total_advances = total_advances
                db.session.commit()
        else:
            continue
    pass


def parse_projects_and_write(projects):
    projects_treated = 0
    # Check requester type and handle accordingly
    for p in projects:
        if p.requester.type in ["PO", "SDC", "LOCATAIRE", "TENANT"]:
            handle_po_tenant_sdc(p)
        elif p.requester.type == "PB":
            handle_pb(p)
        else:
            print(f"project {p.id} has an unknown requester type ({p.requester.type})")
        print(f"Treated project {p.id}")
        projects_treated += 1
    return projects_treated


if __name__ == '__main__':
    with app.app_context():
        from app.project.projects import Project
        # Write headers
        write_csv_headers()
        # Get all projects
        projects = Project.query.all()
        # Write Body
        projects_treated = parse_projects_and_write(projects)
        print(f"Total numbers of project treated: {projects_treated}")
        


# algo

"""
Objectif:
recalculer :
- subvention_on_TTC
- total_advances
- total_subventions
- total_work_price 
- remaining_cost
quand les champs sont vides

Pour chaque projet
    Pour chaque simulation
        - lister les devis et faire la somme des price_incl_tax (champs unique)
        - total_subventions => somme montants_subventions
            => Recalculer systématiquement chaque montant_subventions (dépense subventionnée x taux)
        - total_advances => somme des avances
        - subventions_on_TTC (((total_work_price - remaining_cost) / total_work_price) * 100 arrondi au int au dessus)
        - remaining_cost = total_price_incl_tax - total_subventions
"""



"""
pour chaque projet, check le type
lister les simulations

si po/sdc/locataire
pour chaque simulation, 

faire la somme des simulation_funder.subvention
total_advances = somme simulation_funder.advance
remaining_cost = total_work_price - total_subventions
subvention_on_ttc = ((total_work_price - remaining_cost) / total_work_price) * 100 arrondi au int au dessus

si pb
lister les funder_accommodations
faire les mêmes sommes qu'au dessus
mettre résultats des sommes dans les simulation_sub_result correspondants (même simulation_id et accommodation_id)
faire la somme des sub_results dans simulation

"""
