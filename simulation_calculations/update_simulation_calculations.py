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

def handle_pb(project, failing_accommodations):
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
    from app.project.simulations.model import SimulationQuote

    simulations = project.simulations
    if len(simulations) == 0:
        return
    

    for s in simulations:
        if needs_calculation(s):
            # Get OLD values
            old_total_work_price = s.total_work_price
            old_total_subventions = s.total_subventions
            old_remaining_costs = s.remaining_costs 
            old_subvention_on_TTC = s.subvention_on_TTC
            
            print(f"\n\n========== PB: Simulation {s.id}: recalculating...\n")
            sub_results = {}
            sub_results["common_area"] = {}
            sub_results["common_area"]["total_subvention"] = 0
            sub_results["common_area"]["total_work_price"] = 0

            # Search funder_accommodation from simulation_funder
            # Total_subvention (each accommodation + initial state)
            for sf in s.simulation_funders:
                if len(sf.funder_accommodations) > 0:
                    for fa in sf.funder_accommodations:
                        fa.subvention = calculate_subvention(s, sf, 'PB', fa)
                        if fa.subvention != 0: print(f"Subvention calculated: {fa.subvention} for sf {sf.id}, fa {fa.id}")
                        if fa.is_common_area:
                            sub_results["common_area"]["total_subvention"] += fa.subvention
                        else:
                            if fa.accommodation_id not in sub_results:
                                sub_results[fa.accommodation_id] = {}
                                sub_results[fa.accommodation_id]["total_subvention"] = 0

                            sub_results[fa.accommodation_id]["total_subvention"] += (
                                round(fa.subvention, 2) if fa.subvention is not None else 0
                            )
                        
                else:
                    pass
            
            print("\n")

            # Find quote associated to simulation
            associated_quotes = []
            for quote in s.quotes:
                associated_quote = SimulationQuote.query \
                    .filter(SimulationQuote.base_quote_id == quote.id) \
                    .filter(SimulationQuote.simulation_id == s.id)
                if associated_quote is not None:
                    associated_quotes.append(quote)

            # Total work price (from quotes_accommodation)
            for associated_quote in associated_quotes:
                if len(associated_quote.accommodations) == 0:
                    # Quote with no quotes_accommodations (old useless quote)
                    continue

                sub_results["common_area"]["total_work_price"] += (
                    associated_quote.common_price_incl_tax if associated_quote.common_price_incl_tax else 0
                )
                for qa in associated_quote.accommodations:
                    print(f"Acc n°{qa['quote_accommodation_id']} found:\n{qa}\n")

                    if qa['accommodation'].id not in sub_results:
                        failing_accommodations.append(qa['accommodation'].id)
                        continue
                    
                    if 'total_work_price' not in sub_results[qa['accommodation'].id]:
                        sub_results[qa['accommodation'].id]["total_work_price"] = 0

                    sub_results[qa['accommodation'].id]["total_work_price"] += qa['price_incl_tax']

                    print(f"Sub result calculated:\n{sub_results}\n")
            

            for accommodation in sub_results:
                # Here quotes_accommodations have been found previously
                # And values to calculate subventions exists
                if 'total_work_price' in sub_results[accommodation]:
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
                    print(f"No total_work_price calculated: can't calculate other fields for accommodation n°{accommodation}: ")
            
            total_subventions = [res.get("total_subvention") for res in sub_results.values()]
            total_work_prices = [res.get("total_work_price", 0) for res in sub_results.values()]
            remaining_costs = [res.get("remaining_cost", 0) for res in sub_results.values()]
            subventions_on_ttc = [res.get("subvention_on_ttc", 0) for res in sub_results.values()]
            write_log_in_csv(
                [
                    project.id,
                    s.name,
                    old_total_work_price,
                    functools.reduce(
                        lambda a, b: a + b,
                        total_work_prices
                    ),
                    old_total_subventions,
                    functools.reduce(
                        lambda a, b: a + b,
                        total_subventions
                    ),
                    old_remaining_costs,
                    functools.reduce(
                        lambda a, b: a + b,
                        remaining_costs
                    ),
                    old_subvention_on_TTC,
                    functools.reduce(
                        lambda a, b: a + b,
                        subventions_on_ttc
                    ),
                    "None",
                ]
            )


            # Update Global Simulation
            s.total_subventions = sum(total_subventions)
            s.total_work_price = sum(total_work_prices)
            s.remaining_costs = sum(remaining_costs)
            s.subvention_on_TTC = sum(subventions_on_ttc)
            print(f"- - - - - NEW SIMULATION : {s.id} - - - - - - ")
            print(s.total_subventions)
            print(s.total_work_price)
            print(s.remaining_costs)
            print(s.subvention_on_TTC)
            print("- - - - - - - - - - - - - - - - - - - -")

            # Update each Sub Result
            sub_results_query = SimulationSubResult.query.filter(SimulationSubResult.simulation_id == s.id)
            for accommodation in sub_results:
                sub_results_item = None
                if accommodation != "common_area":
                    sub_results_item = sub_results_query.filter(SimulationSubResult.accommodation_id == accommodation).first()
                else:
                    sub_results_item = sub_results_query.filter(SimulationSubResult.is_common_area == True).first()

                if sub_results_item:
                    print(f"- - - - - OLD SUB ITEM : {sub_results_item.id} - - - - ")
                    print(sub_results_item.total_subvention)
                    print(sub_results_item.work_price)
                    print(sub_results_item.remaining_cost)
                    print(sub_results_item.subvention_on_TTC)

                    sub_results_item.total_subvention = round(sub_results[accommodation]['total_subvention'], 2)
                    if "total_work_price" in sub_results[accommodation]:
                        sub_results_item.work_price = round(sub_results[accommodation]['total_work_price'], 2)
                    if "remaining_cost" in sub_results[accommodation]:
                        sub_results_item.remaining_cost = round(sub_results[accommodation]['remaining_cost'], 2)
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
            # Get OLD values
            old_total_work_price = s.total_work_price
            old_total_subventions = s.total_subventions
            old_remaining_costs = s.remaining_costs 
            old_subvention_on_TTC = s.subvention_on_TTC
            old_total_advances = s.total_advances

            print(f"\n\n========== PO: Simulation {s.id}: recalculating...\n")
            total_subventions = 0
            total_advances = 0
            total_work_price = 0
            remaining_cost = 0
            subvention_on_ttc = 0

            for sf in s.simulation_funders:
                # Total subventions
                sf.subvention = calculate_subvention(s, sf, 'PO')
                if sf.subvention != 0: print(f"Subvention calculated: {sf.subvention} for sf {sf.id}")
                total_subventions += sf.subvention

                # Total advances
                total_advances += advances_for_po_sdc_loc(s, sf)

            print(f"Total advances calculated: {total_advances}\n")

            # Total work price (from quotes)
            total_work_price = get_total_price_incl_tax(s)

            # Remaining cost
            if total_work_price - total_subventions < 0:
                remaining_cost = 0
            else:
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
                    old_total_work_price,
                    total_work_price,
                    old_total_subventions,
                    total_subventions,
                    old_remaining_costs,
                    remaining_cost,
                    old_subvention_on_TTC,
                    subvention_on_ttc,
                    old_total_advances,
                    total_advances,
                ]
            )

            # Update Global Simulation
            s.total_work_price = total_work_price
            s.total_subventions = total_subventions
            s.remaining_costs = remaining_cost
            s.subvention_on_TTC = subvention_on_ttc
            s.total_advances = total_advances
            print(f"- - - - - NEW SIMULATION : {s.id} - - - - - - ")
            print(s.total_subventions)
            print(s.total_work_price)
            print(s.remaining_costs)
            print(s.subvention_on_TTC)
            print("- - - - - - - - - - - - - - - - - - - -")

            if not DRY_RUN:
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
    failing_accommodations = []
    # Check requester type and handle accordingly
    for p in projects:
        if p.requester.type in ["PO", "SDC", "LOCATAIRE", "TENANT"]:
            handle_po_tenant_sdc(p)
            pass
        elif p.requester.type == "PB":
            handle_pb(p, failing_accommodations)
            pass
        else:
            unknown.append(p.id)
            # print(f"project {p.id} has an unknown requester type ({p.requester.type})")
        # print(f"Project treated: n°{p.id}")
        projects_treated += 1
    print("Failing accommodations", failing_accommodations)
    return projects_treated, unknown


if __name__ == '__main__':
    with app.app_context():
        from app.project.projects import Project
        # Write headers
        write_csv_headers()
        # Get all projects
        # projects = Project.query.all()
        # Test
        projects = [Project.query.filter(Project.id == 345).first()]
        # Write Body
        projects_treated, unknown = parse_projects_and_write(projects)
        print(f"Total numbers of project treated: {projects_treated}")
        print(f"Projects with unknown requester types: {unknown}")
        