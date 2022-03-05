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