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
    """
    PB
    Pour chaque projet
        Pour chaque simulation
            - Parcourir les simulations_funders
                - Parcourir les funder_accommodation associés
                    - Calcul de la subvention pour le logement (si le calcul est possible )
                    - Ajout d'un objet common_area OU l'id du logement contenu dans l'objet
                     et ajout de la subvention à la somme (si il existe un logement pour le funder accommodation)
            - Parcourir les devis
                - Parcourir devis de logement associés (si ils existent)
                    - Somme des work price pour common area et chaque logement
            - Calcul des remaining cost + subvention_on_ttc pour chaque logement inséré dans l'objet jusqu'a présent (si calcul possible)
    """
    from app.project.simulations.model import SimulationSubResult
    from app.project.simulations.model import Simulation

    simulations = project.simulations
    if len(simulations) == 0:
        return

    for s in simulations:
        if needs_calculation(s):
            sub_results = {}
            sub_results["common_area"] = {}
            sub_results["common_area"]["total_subvention"] = 0
            sub_results["common_area"]["total_work_price"] = 0

            # Search funder_accommodation from simulation_funder
            # Total_subvention (each accommodation + initial state)
            for sf in s.simulation_funders:
                if len(sf.funder_accommodations) > 0:
                    for fa in sf.funder_accommodations:
                        print(f"NEW FA {fa.id}")
                        
                        if no_missing_values(fa):
                            fa.subvention = calculate_subvention(fa)
                            if fa.is_common_area:
                                sub_results["common_area"]["total_subvention"] += (
                                    fa.subvention if fa.subvention is not None else 0
                                )
                            else:
                                if fa.accommodation_id not in sub_results:
                                    sub_results[fa.accommodation_id] = {}
                                    sub_results[fa.accommodation_id]["total_subvention"] = 0

                                sub_results[fa.accommodation_id]["total_subvention"] += (
                                    round(fa.subvention, 2) if fa.subvention is not None else 0
                                )
                        elif fa.accommodation_id:
                            if fa.accommodation_id not in sub_results:
                                sub_results[fa.accommodation_id] = {}
                                sub_results[fa.accommodation_id]["total_subvention"] = 0
                else:
                    pass


            # Total work price (from quotes_accommodation)
            for quote in s.quotes:
                if len(quote.accommodations) == 0:
                    # Quote with no quotes_accommodations (old useless quote)
                    continue
                for qa in quote.accommodations:
                    sub_results["common_area"]["total_work_price"] += (
                        quote.common_price_incl_tax if quote.common_price_incl_tax else 0
                    )

                    # Specific case: accommodation_id doesn't exist in funder_accommodation parsed
                    if qa['accommodation'].id not in sub_results:
                        print(qa['accommodation'].id)
                        print(sub_results)
                        continue
                    
                    if 'total_work_price' not in sub_results[qa['accommodation'].id]:
                        sub_results[qa['accommodation'].id]["total_work_price"] = 0

                    sub_results[qa['accommodation'].id]["total_work_price"] += qa['price_incl_tax']
            

            for accommodation in sub_results:
                # Here quotes_accommodations have been found previously
                # And values to calculate subventions exists
                if 'total_work_price' in sub_results[accommodation] and \
                   sub_results[accommodation]['total_subvention'] is not None :
                    # Build remaining cost
                    if sub_results[accommodation]["total_subvention"] > sub_results[accommodation]["total_work_price"]:
                        sub_results[accommodation]['remaining_cost'] = 0
                    else:
                        sub_results[accommodation]['remaining_cost'] = abs(
                            round(
                                sub_results[accommodation]["total_work_price"] - sub_results[accommodation]["total_subvention"],
                                2
                            )
                        )
                    # Build subvention_on_ttc
                    if sub_results[accommodation]["total_work_price"] == 0:
                        # % to 0 if work_price = 0
                        sub_results[accommodation]["subvention_on_ttc"] = 0
                    else:
                        sub_results[accommodation]["subvention_on_ttc"] = round(
                            (
                                (
                                    sub_results[accommodation]["total_work_price"]
                                    - sub_results[accommodation]["remaining_cost"]
                                )
                                / sub_results[accommodation]["total_work_price"]
                            )
                            * 100,
                            0,
                        )
                else:
                    print(f"Missing data for accommodation n°{accommodation}")
            
            total_subventions = [res.get("total_subvention") for res in sub_results.values()]
            total_work_prices = [res.get("total_work_price", 0) for res in sub_results.values()]
            remaining_costs = [res.get("remaining_cost", 0) for res in sub_results.values()]
            subventions_on_ttc = [res.get("subvention_on_ttc", 0) for res in sub_results.values()]
            write_log_in_csv(
                [
                    project.id,
                    s.name,
                    functools.reduce(
                        lambda a, b: a + b,
                        total_subventions
                    ),
                    functools.reduce(
                        lambda a, b: a + b,
                        total_work_prices
                    ),
                    functools.reduce(
                        lambda a, b: a + b,
                        remaining_costs
                    ),
                    functools.reduce(
                        lambda a, b: a + b,
                        subventions_on_ttc
                    ),
                    "None",
                ]
            )


            # Update Global Simulation
            simulation = Simulation.query.filter(Simulation.id == s.id).first()
            print(f"- - - - - OLD SIMULATION : {simulation.id} - - - - ")
            print(simulation.total_subventions)
            print(simulation.total_work_price)
            print(simulation.remaining_costs)
            print(simulation.subvention_on_TTC)
            simulation.total_subventions = sum(total_subventions)
            simulation.total_work_price = sum(total_work_prices)
            simulation.remaining_costs = sum(remaining_costs)
            simulation.subvention_on_TTC = sum(subventions_on_ttc)
            print(f"- - - - - NEW SIMULATION : {simulation.id} - - - - - - ")
            print(simulation.total_subventions)
            print(simulation.total_work_price)
            print(simulation.remaining_costs)
            print(simulation.subvention_on_TTC)

            # Update each Sub Result
            sub_results_query = SimulationSubResult.query.filter(SimulationSubResult.simulation_id == s.id)
            for accommodation in sub_results:
                if accommodation != "common_area":
                    sub_results_item = sub_results_query.filter(SimulationSubResult.accommodation_id == accommodation).first()
                    if sub_results_item:
                        print(f"- - - - - OLD SUB ITEM : {sub_results_item.id} - - - - ")
                        print(sub_results_item.total_subvention)
                        print(sub_results_item.work_price)
                        print(sub_results_item.remaining_cost)
                        print(sub_results_item.subvention_on_TTC)

                        sub_results_item.total_subvention = sub_results[accommodation]['total_subvention']
                        if "total_work_price" in sub_results[accommodation]:
                            sub_results_item.work_price = sub_results[accommodation]['total_work_price']
                        if "remaining_cost" in sub_results[accommodation]:
                            sub_results_item.remaining_cost = sub_results[accommodation]['remaining_cost']
                        if "subvention_on_ttc" in sub_results[accommodation]:
                            sub_results_item.subvention_on_TTC = sub_results[accommodation]['subvention_on_ttc']

                        print(f"- - - - - NEW SUB ITEM : {sub_results_item.id} - - - - ")
                        print(sub_results_item.total_subvention)
                        print(sub_results_item.work_price)
                        print(sub_results_item.remaining_cost)
                        print(sub_results_item.subvention_on_TTC)

        if not DRY_RUN:
            db.session.commit()

def handle_po_tenant_sdc(project):
    """
    PO/SDC/Tenant
    Pour chaque projet
        Pour chaque simulation
            - lister les devis et faire la somme des price_incl_tax (champs unique)
            - total_subventions => somme montants_subventions
                => Recalculer systématiquement chaque montant_subventions (dépense subventionnée x taux)
            - total_advances => somme des avances
            - subventions_on_TTC (((total_work_price - remaining_cost) / total_work_price) * 100 arrondi au int au dessus)
            - remaining_cost = total_work_price - total_subventions
    """
    simulations = project.simulations
    if len(simulations) == 0:
        return

    for s in simulations:
        if needs_calculation(s):
            total_subventions = 0
            total_advances = 0
            total_work_price = 0
            remaining_cost = 0
            subvention_on_ttc = 0

            for sf in s.simulation_funders:
                # Total subventions
                if no_missing_values(sf):
                    sf.subvention = calculate_subvention(sf)
                    total_subventions += sf.subvention
                # Total advances
                total_advances += sf.advance if sf.advance else 0

            # Total work price (from quotes)
            total_work_price = get_total_price_incl_tax(s)

            # Remaining cost
            remaining_cost = total_work_price - total_subventions

            # Subvention on ttc
            if total_work_price != 0:
                subvention_on_ttc = round(
                    ((total_work_price - remaining_cost) / total_work_price) * 100,
                    0,
                )

            write_log_in_csv(
                [
                    project.id,
                    s.name,
                    total_work_price,
                    total_subventions,
                    remaining_cost,
                    subvention_on_ttc,
                    total_advances,
                ]
            )
            if not DRY_RUN:
                s.total_work_price = total_work_price
                s.total_subventions = total_subventions
                s.remaining_costs = remaining_cost
                s.subvention_on_TTC = subvention_on_ttc
                s.total_advances = total_advances
                db.session.commit()
        else:
            continue
    pass


def parse_projects_and_write(projects):
    """
    Objectif:
        Pour chaque projet, en fonction du type de requester, recalculer :
        - subvention_on_TTC
        - total_advances
        - total_subventions
        - total_work_price 
        - remaining_cost
        quand les champs sont vides
        pour chaque simulation 
    """
    projects_treated = 0
    unknown = []
    # Check requester type and handle accordingly
    for p in projects:
        if p.requester.type in ["PO", "SDC", "LOCATAIRE", "TENANT"]:
            handle_po_tenant_sdc(p)
        elif p.requester.type == "PB":
            handle_pb(p)
        else:
            unknown.append(p.id)
            print(f"project {p.id} has an unknown requester type ({p.requester.type})")
        # print(f"Project treated: n°{p.id}")
        projects_treated += 1
    return projects_treated, unknown


if __name__ == '__main__':
    with app.app_context():
        from app.project.projects import Project
        # Write headers
        write_csv_headers()
        # Get all projects
        projects = Project.query.all()
        # Test
        # projects = [Project.query.filter(Project.id == 2007).first()]
        # Write Body
        projects_treated, unknown = parse_projects_and_write(projects)
        print(f"Total numbers of project treated: {projects_treated}")
        print(f"Projects with unknown requester types: {unknown}")
        