from app import create_app

app = create_app("dev")

with app.app_context():
    from app.mission.missions import Mission
    missions = Mission.query.all()
    print()

# fields impacted : 
# SIMULATION_FUNDER : 
# eligible_cost
# remaining_cost
# subvention
# subvention_on_ttc
# upper_limit
# work_price

# SIMULATION
# total_work_price = somme quote.price_incl_tax
# total_subventions = somme simulation_funder.subvention pour cette simulation
# remaining_cost = total_work_price - total_subventions
# subvention_on_ttc = ((total_work_price - remaining_cost) / total_work_price) * 100 arrondi au int au dessus
# total_advances = somme simulation_funder.advance pour cette simulation
