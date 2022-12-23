from market.models import *
import pandas as pd
df = pd.DataFrame(User.objects.all().values_list('id', 'last_login', 'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email', 'phone_number', 'avatar', 'email_verified', 'phone_verified', 'balance', 'is_business'), columns=['id', 'last_login', 'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email', 'phone_number', 'avatar', 'email_verified', 'phone_verified', 'balance', 'is_business']
for tzcol in tz_col:
	df[tzcol] = df[tzcol].apply(lambda r: r.replace(tzinfo=None))
df.to_excel('output.xlsx')
