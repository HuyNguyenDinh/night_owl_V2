from tests.market.fixtures.models.base_recipes import general_bill

payed_bill = general_bill.extend(payed=True)
not_payed_bill = general_bill.extend(payed=False)