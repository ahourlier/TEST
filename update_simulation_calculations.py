from unicodedata import name
from app import create_app, db

app = create_app("dev")

DRY_RUN = True


def get_total_price_incl_tax(simulation):
    total_price_incl_tax = 0
    for quote in simulation.quotes:
        total_price_incl_tax += quote.price_incl_tax
    return total_price_incl_tax


def needs_calculation(s):
    return (
        s.remaining_costs is None
        and s.subvention_on_TTC is None
        and s.total_advances is None
        and s.total_subventions is None
        and s.total_work_price is None
    )


def subvention_needs_calculation(simulation_funder):
    return (
        simulation_funder.subvention is None
        and simulation_funder.subventioned_expense is not None
        and simulation_funder.rate is not None
    )

def calculate_subvention(simulation_funder):
    return (simulation_funder.subventioned_expense * simulation_funder.rate) / 100


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
                    "subvention_on_ttc": 0
                }
            sub_results[None] = {
                    "price_incl_tax": 0,
                    "total_subvention": 0,
                    "remaining_cost": 0,
                    "subvention_on_ttc": 0
                }
            for quote in s.quotes:
                for quote_accommodation in quote.accommodations:
                    sub_results[quote_accommodation["accommodation"].id]["price_incl_tax"] += quote_accommodation["price_incl_tax"]
            for sf in s.simulation_funders:
                if len(sf.funder_accommodations) > 0:
                    for fa in sf.funder_accommodations:
                        if subvention_needs_calculation(fa):
                            fa.subvention = calculate_subvention(fa)
                        sub_results[fa.accommodation_id]["total_subvention"] += fa.subvention
                else:
                    pass
            pass

            
            # for sf in s.simulation_funders:
            #     funder_accommodations = sf.funder_accommodations
            #     for fa in funder_accommodations:
            #         sub_result_query = SimulationSubResult.query.filter(
            #             SimulationSubResult.simulation_id == s.id
            #         )
            #         if fa.is_common_area:
            #             sub_result_query = SimulationSubResult.query.filter(
            #                 SimulationSubResult.is_common_area == True
            #             )
            #         else:
            #             sub_result_query = SimulationSubResult.query.filter(
            #                 SimulationSubResult.accommodation_id == fa.accommodation_id
            #             )
            #         sub_result = sub_result_query.first()
            #         price_incl_tax = 0
            #         total_subvention = 0
            #         remaining_cost = 0
            #         subvention_on_ttc = 0
            #         if subvention_needs_calculation(fa):
            #             fa.subvention = calculate_subvention(fa)
                    

    # for s in simulations:
    #     if needs_calculation(s):

    #         for sf in s.simulation_funders:
    #             funder_accommodations = sf.funder_accommodations
    #             sf_subvention = 0
    #             for fa in funder_accommodations:
    #                 # sub_result_query = SimulationSubResult.query.filter(
    #                 #     SimulationSubResult.simulation_id == s.id
    #                 # )
    #                 # if fa.is_common_area:
    #                 #     sub_result_query = SimulationSubResult.query.filter(
    #                 #         SimulationSubResult.is_common_area == True
    #                 #     )
    #                 # else:
    #                 #     sub_result_query = SimulationSubResult.query.filter(
    #                 #         SimulationSubResult.accommodation_id == fa.accommodation_id
    #                 #     )
    #                 # sub_result = sub_result_query.first()
    #                 if subvention_needs_calculation(fa):
    #                     fa.subvention = calculate_subvention(fa)
    #                 sf_subvention +=  fa.subvention if fa.subvention is not None else 0
    #             if sf.subvention in [0, None] and sf_subvention > 0:
    #                 sf.subvention = sf_subvention
    #             pass
    #     else:
    #         continue


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

                if subvention_needs_calculation(sf):
                    sf.subvention = calculate_subvention(sf)

                total_subventions += sf.subvention if sf.subvention else 0
                total_advances += sf.advance if sf.advance else 0
            remaining_cost = total_price_incl_tax - total_subventions
            subvention_on_ttc = round(
                ((total_price_incl_tax - remaining_cost) / total_price_incl_tax) * 100,
                0,
            )
            print(f"CHANGES ON PROJECT {project.id}")
            print(f"AND SIMULATION {s.name}")
            print(f"total_work_price : {total_price_incl_tax}")
            print(f"total_subventions : {total_subventions}")
            print(f"remaining_cost : {remaining_cost}")
            print(f"subvention_on_TTC : {subvention_on_ttc}")
            print(f"total_advances : {total_advances}")
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


with app.app_context():
    from app.project.projects import Project

    projects = Project.query.all()
    projects_treated = 0
    for p in projects:
        if p.requester.type in ["PO", "SDC", "LOCATAIRE"]:
            handle_po_tenant_sdc(p)
        elif p.requester.type == "PB":
            handle_pb(p)
        else:
            print(f"project {p.id} has an unknown requester type ({p.requester.type})")
    print()


# algo
"""
pour chaque projet, check le type
lister les simulations

si po/sdc/locataire
pour chaque simulation, lister les devis et faire la somme des price_incl_tax
faire la somme des simulation_funder.subvention
total_advances = somme simulation_funder.advance
remaining_cost = total_work_price - total_subventions
subvention_on_ttc = ((total_work_price - remaining_cost) / total_work_price) * 100 arrondi au int au dessus

si pb
lister les funder_accommodations
faire les mêmes sommes qu'au dessus
mettre résultats des sommes dans les simulation_sub_result correspondants (même simulation_id et accommodation_id)
faire la somme des sub_results dans simulation



si pb
pour chaque simulation
"""
