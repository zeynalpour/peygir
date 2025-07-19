#app/services/external_api.py

'''
شبیه سازی API خارجی
'''

import random

def fetch_tasks():
    '''
    این تابع هر مرتبه 4 تسک رندوم از 110 تا 119 برمیگرداند.
    '''
    sample_ids = [f"task_{i}" for i in range(110, 119)]
    return random.sample(sample_ids, k=4)  
