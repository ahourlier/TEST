def get_total_price_incl_tax(simulation):
    total_price_incl_tax = 0
    for quote in simulation.quotes:
        if quote.price_incl_tax:
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

def no_missing_values(f):
    """
    'f' can be funder_accommodation or simulation_funder
    """
    return f.subventioned_expense and f.rate

def subvention_needs_calculation(simulation_funder):
    return (
        simulation_funder.subvention is None
        and simulation_funder.subventioned_expense is not None
        and simulation_funder.rate is not None
    )


def calculate_subvention(simulation_funder):
    """
    Pour PB:
        - Les deux valeurs sont remplies 
            Calcul via funder_accommodation
        - Le rate uniquement est NULL
            Calcul avec le rate de funding_scenario
                   avec le subventioned_expense de funder_accommodation

        - Le subventioned_expense uniquement est NULL


            SUM(quote_accommodation.eligible_amount) => Tous les eligible amount du logement (listing des devis)

            (financeurlogement.rate / 100) *
            LEAST(
                SUM(quote_accommodation.eligible_amount),
                (
                    financeurscenario.upper_price_surface_limit *
                    LEAST(
                        logement.living_area + LEAST(IFNULL(logement.additional_area / 2, 0), 8),
                        financeurscenario.upper_surface_limit
                    )
                )
            )

        - les deux sont Null

            (financeurscenario.rate / 100) *
            LEAST(
                SUM(quote_accommodation.eligible_amount),
                (
                    financeurscenario.upper_price_surface_limit *
                    LEAST(
                        logement.living_area + LEAST(IFNULL(logement.additional_area / 2, 0), 8),
                        financeurscenario.upper_surface_limit
                    )
                )
            )


    PO 

    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT') AND simulationfinanceur.subventioned_expense IS NOT NULL AND simulationfinanceur.rate IS NOT NULL 
      THEN (simulationfinanceur.rate / 100) * MAX(simulationfinanceur.subventioned_expense)
    
    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT') AND simulationfinanceur.subventioned_expense IS NOT NULL AND simulationfinanceur.rate IS NULL 
      THEN (financeurscenario.rate / 100) * MAX(simulationfinanceur.subventioned_expense)

    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT') AND simulationfinanceur.subventioned_expense IS NULL AND simulationfinanceur.rate IS NOT NULL 
    (financeurlogement.rate / 100) * LEAST(SUM(devis.eligible_amount), financeurscenario.upper_limit)

    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT') AND simulationfinanceur.subventioned_expense IS NULL 
      THEN (financeurscenario.rate / 100) * LEAST(SUM(devis.eligible_amount), financeurscenario.upper_limit)
    ELSE NULL

    """
    return (simulation_funder.subventioned_expense * simulation_funder.rate) / 100