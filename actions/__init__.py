import random
import pandas as pd
import string 
insurance_ids = [
    'ABC1234',
    'XYZ5678',
    'DEF9012',
    'GHI3456',
    'JKL7890',
    'MNO2345',
    'PQR6789',
    'STU0123',
    'VWX4567',
    'YZA8901',
    'BCD2345',
    'EFG6789',
    'HIJ0123',
    'KLM4567',
    'NOP8901',
    'QRS2345',
    'TUV6789', 
    'WXY0123',
    'ZAB4567',
    'CDE8901'
]
claim_ids = [
    'AB12345',
    'CD67890',
    'EF23456',
    'GH78901',
    'IJ34567',
    'KL89012',
    'MN45678',
    'OP90123',
    'QR56789',
    'ST01234',
    'UV67890',
    'WX23456',
    'YZ78901',
    'AB34567',
    'CD89012',
    'EF45678',
    'GH90123',
    'IJ56789',
    'KL01234',
    'MN67890'
]



amounts = [random.randint(1, 50000) for _ in range(20)]
df=pd.DataFrame(columns=["insurance_ids", "claim_ids"])
for i in range(20):
    new_row = {'insurance_ids': insurance_ids[i], 'claim_ids': claim_ids[i]}
    df.loc[len(df)] = new_row
df.to_csv("data.csv",index=False)
df1=pd.DataFrame(columns=["claim_ids","amounts"])
for i in range(20):
    new_row = {'claim_ids': claim_ids[i], 'amounts':amounts[i]}
    df1.loc[len(df1)] = new_row
df1.to_csv('claims.csv',index=False)