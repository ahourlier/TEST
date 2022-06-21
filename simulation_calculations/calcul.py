def needs_calculation(s):
    return (
        s.remaining_costs is None
        or s.subvention_on_TTC is None
        or s.total_advances is None
        or s.total_subventions is None
        or s.total_work_price is None
    )


def get_total_price_incl_tax(simulation):
    total_price_incl_tax = 0
    for quote in simulation.quotes:
        if quote.price_incl_tax:
            total_price_incl_tax += quote.price_incl_tax
    return total_price_incl_tax


def get_total_quotes_eligible_amount(simulation):
    """
        Find quote associated to simulation, and get sum of eligible amount
    """
    from app.project.simulations.model import SimulationQuote
    total_quote_eligible_amount = 0
    associated_quotes = []

    for quote in simulation.quotes:
        associated_quote = SimulationQuote.query \
            .filter(SimulationQuote.base_quote_id == quote.id) \
            .filter(SimulationQuote.simulation_id == simulation.id)
        if associated_quote is not None:
            associated_quotes.append(quote)
    
    for elem in associated_quotes:
        total_quote_eligible_amount += elem.eligible_amount
    
    return total_quote_eligible_amount


def subvention_for_po_sdc_loc(simulation, sf):
    """
    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT' OR demandeur.type = 'SDC') AND simulationfinanceur.subventioned_expense IS NOT NULL AND simulationfinanceur.rate IS NOT NULL 
      THEN (simulationfinanceur.rate / 100) * MAX(simulationfinanceur.subventioned_expense)
    
    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT' OR demandeur.type = 'SDC') AND simulationfinanceur.subventioned_expense IS NOT NULL AND simulationfinanceur.rate IS NULL 
      THEN (financeurscenario.rate / 100) * MAX(simulationfinanceur.subventioned_expense)

    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT' OR demandeur.type = 'SDC') AND simulationfinanceur.subventioned_expense IS NULL AND simulationfinanceur.rate IS NOT NULL 
    (financeurlogement.rate / 100) * LEAST(SUM(devis.eligible_amount), financeurscenario.upper_limit)

    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT' OR demandeur.type = 'SDC') AND simulationfinanceur.subventioned_expense IS NULL 
      THEN (financeurscenario.rate / 100) * LEAST(SUM(devis.eligible_amount), financeurscenario.upper_limit)
    ELSE NULL
    """
    from app.funder.funding_scenarios.model import FundingScenario

    if sf.subventioned_expense and sf.rate:
        return (sf.rate / 100) * sf.subventioned_expense
    if sf.subventioned_expense and not sf.rate:
        if sf.match_scenario_id:
            fs = FundingScenario.query.filter(FundingScenario.id == sf.match_scenario_id).first()
            return (fs.rate / 100) * sf.subventioned_expense
        else:
            print(f'Can\'t calculate subventions: No rate AND no matching funding scenario from sf n°{sf.id}, simulation n°{simulation.id}')
            return 0
    if not sf.subventioned_expense and sf.rate:
        print(f'Never happens')
        fa = sf.funder_accommodations
        if len(fa) > 0:
            print(fa)
            # N'arrive jamais
            # (financeurlogement.rate / 100) * LEAST(SUM(devis.eligible_amount), financeurscenario.upper_limit)
        else:
            print(f'Can\'t calculate subventions: No funder accommodation exists')
        return 0
    if not sf.subventioned_expense and not sf.rate:
        if sf.match_scenario_id:
            # Get FundingScenario
            fs = FundingScenario.query.filter(FundingScenario.id == sf.match_scenario_id).first()
            # Get Sum of eligible amount for quotes
            total_quotes_eligible_amount = get_total_quotes_eligible_amount(simulation)
            return (fs.rate / 100) * min(total_quotes_eligible_amount, fs.upper_limit)
        else:
            print(f'Can\'t calculate subventions: No rate, no subventioned_expense AND no matching funding scenario from sf n°{sf.id}, simulation n°{simulation.id}')
            return 0



def advances_for_po_sdc_loc(simulation, sf):
    """
    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT' OR demandeur.type = 'SDC') AND simulationfinanceur.advance IS NOT NULL
      THEN simulationfinanceur.advance

    WHEN (demandeur.type = 'PO' OR demandeur.type = 'TENANT' OR demandeur.type = 'SDC') AND simulationfinanceur.advance IS NULL
    (financeurscenario.advance / 100) * simulationfinanceur.subvention
    """
    from app.funder.funding_scenarios.model import FundingScenario

    if sf.advance:
        return sf.advance
    if not sf.advance:
        # Get FundingScenario
        fs = FundingScenario.query.filter(FundingScenario.id == sf.match_scenario_id).first()
        if not fs: 
            print(f'Can\'t calculate advances: No matching funding scenario from sf n°{sf.id}, simulation n°{simulation.id}')
            return 0
        return (fs.advance / 100) * sf.subvention
    return 0


def get_total_quotes_accommodations_eligible_amount(simulation):
    """
        Find quote associated to simulation,
        then quotes_accommodations associated to found quotes
        and get sum of eligible amount
    """
    from app.project.simulations.model import SimulationQuote
    total_quote_accommodations_eligible_amount = 0
    associated_quotes = []

    for quote in simulation.quotes:
        associated_quote = SimulationQuote.query \
            .filter(SimulationQuote.base_quote_id == quote.id) \
            .filter(SimulationQuote.simulation_id == simulation.id)
        if associated_quote is not None:
            associated_quotes.append(quote)
    
    for quote in associated_quotes:
        for qa in quote.accommodations:
            total_quote_accommodations_eligible_amount += qa['eligible_amount']
    
    return total_quote_accommodations_eligible_amount

def subvention_for_pb(simulation, sf, fa):
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
    """
    from app.funder.funding_scenarios.model import FundingScenario

    if fa.subventioned_expense and fa.rate:
        return (fa.rate / 100) * fa.subventioned_expense
    if fa.subventioned_expense and not fa.rate:
        if sf.match_scenario_id:
            fs = FundingScenario.query.filter(FundingScenario.id == sf.match_scenario_id).first()
            return (fs.rate / 100) * fa.subventioned_expense
        else:
            print(f'Can\'t calculate subventions: No rate from fa n°{fa.id} AND no matching funding scenario from sf n°{sf.id}, simulation n°{simulation.id}')
            return 0
    if not fa.subventioned_expense and fa.rate:
        # Get total eligible amount from quotes_accommodations
        total_quotes_accommodations_eligible_amount = get_total_quotes_accommodations_eligible_amount(simulation)
        # Get Funding Scenario
        if sf.match_scenario_id:
            fs = FundingScenario.query.filter(FundingScenario.id == sf.match_scenario_id).first()
            # Get Accommodation from FunderAccommodation
            acc = fa.accommodation
            if acc:
                if acc.living_area and acc.additional_area:
                    return (
                        fa.rate / 100) * \
                        min(
                            total_quotes_accommodations_eligible_amount,
                            fs.upper_price_surface_limit * min(
                                acc.living_area + min(acc.additional_area / 2 if acc.additional_area else 0, 8),
                                fs.upper_surface_limit
                            )
                        )
                else:
                    print(f'Can\'t calculate subventions: No subventioned_expense AND missing value in accommodation n°{acc.id} from fa n°{fa.id}, simulation n°{simulation.id}')
                    return 0
            else:
                print(f'Can\'t calculate subventions: No subventioned_expense AND no accommodation from fa n°{fa.id}, simulation n°{simulation.id}')
                return 0
        else:
            print(f'Can\'t calculate subventions: No subventioned_expense from fa n°{fa.id} AND no matching funding scenario from sf n°{sf.id}, simulation n°{simulation.id}')
            return 0

    if not fa.subventioned_expense and not fa.rate:
        # Get total eligible amount from quotes_accommodations
        total_quotes_accommodations_eligible_amount = get_total_quotes_accommodations_eligible_amount(simulation)
        # Get Funding Scenario
        if sf.match_scenario_id:
            fs = FundingScenario.query.filter(FundingScenario.id == sf.match_scenario_id).first()
            # Get Accommodation from FunderAccommodation
            acc = fa.accommodation
            if acc:
                if acc.living_area and acc.additional_area:
                    return (
                        fs.rate / 100) * \
                        min(
                            total_quotes_accommodations_eligible_amount,
                            fs.upper_price_surface_limit * min(
                                acc.living_area + min(acc.additional_area / 2 if acc.additional_area else 0, 8),
                                fs.upper_surface_limit
                            )
                        )
                else:
                    print(f'Can\'t calculate subventions: No rate, no subventioned_expense from fa n°{fa.id} AND missing value in accommodation n°{acc.id} from fa n°{fa.id}, simulation n°{simulation.id}')
                    return 0
            else:
                print(f'Can\'t calculate subventions: No rate, no subventioned_expense from fa n°{fa.id} AND no accommodation from fa n°{fa.id}, simulation n°{simulation.id}')
                return 0
        else:
            print(f'Can\'t calculate subventions: No rate, no subventioned_expense from fa n°{fa.id} AND no matching funding scenario from sf n°{sf.id}, simulation n°{simulation.id}')
            return 0


def calculate_subvention(simulation, simulation_funder, requester_type, funder_accommodation = None):
    if requester_type != 'PB':
        return subvention_for_po_sdc_loc(simulation, simulation_funder)
    else:
        return subvention_for_pb(simulation, simulation_funder, funder_accommodation)