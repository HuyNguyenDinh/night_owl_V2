from market.baker_recipes import general_voucher
percentage_voucher = general_voucher.extend(is_percentage=True)
not_percentage_voucher = general_voucher.extend(is_percentage=False)