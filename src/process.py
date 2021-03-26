from datetime import datetime, timedelta
import pandas as pd
import math


def find_active_cases_in_date(cases_by_date, date):
    """Return active cases in provided date or before"""
    if date in cases_by_date:
        return cases_by_date.get(date)
    else:
        d = datetime.strptime(date, '%Y-%m-%d')
        k = 1
        while k<20:
            d = d-timedelta(days=1)
            d_formatted = datetime.strftime(d, '%Y-%m-%d')
            if d_formatted in cases_by_date:
                return cases_by_date.get(d_formatted) 
            k = k+1
        

def process():

    # Get Active cases per comuna
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv')
    active_cases_comuna = {}
    for i, j in df.iterrows(): 
        comuna_code = j[3]
        if not comuna_code or math.isnan(comuna_code):
            continue
        comuna_code = int(comuna_code)
        
        
        region = j[0]
        region_code = j[1]
        comuna = j[2]
        population = j[4]
        date = j[5]
        active_cases = int(j[6])
        if not comuna_code in active_cases_comuna:
            active_cases_comuna[comuna_code] = {
                'region_code': region_code,
                'comuna_code': comuna_code,
                'comuna': comuna,
                'region': region,
                'population': population,
                'cases_by_date': {} 
            }
        active_cases_comuna[comuna_code]['cases_by_date'][date] = active_cases
        

    # Get Periods per comuna and step
    df = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto74/paso_a_paso.csv')

    
    dates = list(df.iloc[0:0, 5:].columns)
    last_date = dates[-1]
    
    comunas_data={}
    for i, j in df.iterrows(): 
        region_code = j[0]
        region = j[1]
        comuna_code = j[2]
        comuna = j[3]
        zone = j[4]
        current_step = 0
        periods = []
        period = None
        cols = list(j)[5:]
        for k, c in enumerate(cols):
            if current_step != c \
                or k == len(cols)-1:
                if period:
                    end = dates[k]
                    active_cases_end = find_active_cases_in_date(active_cases_comuna.get(comuna_code).get('cases_by_date'), end)
                    period = {
                        **period,
                        **{
                            'end': end,
                            'active_cases_end': active_cases_end,
                            'delta_active_cases': active_cases_end-period.get('active_cases_start'),
                            'pct_delta_active_cases': (
                                (active_cases_end / max(period.get('active_cases_start'), 1))-1
                            )*100,
                            'current': 1 if end == last_date else 0,
                        }
                    }
                    periods.append(period)
                start = dates[k]
                active_cases_start = find_active_cases_in_date(active_cases_comuna.get(comuna_code).get('cases_by_date'), start)
                period = {
                    'step': c,
                    'start':start,
                    'active_cases_start':active_cases_start,
                }
                current_step = c
        comunas_data[f'{comuna_code}-{zone}'] = {
            'region_code': region_code,
            'comuna_code': comuna_code,
            'comuna': comuna,
            'region': region,
            'zone': zone,
            'periods': periods
        }

    rows = []
    for k, v in comunas_data.items():
        for b in v.get('periods'):
            row = {
                'region_code': v.get('region_code'),
                'region': v.get('region'),
                'comuna_code': v.get('comuna_code'),
                'comuna': v.get('comuna'),
                'zone': v.get('zone'),
                'step': b.get('step'),
                'start': b.get('start'),
                'end': b.get('end'),
                'active_cases_start': b.get('active_cases_start'),
                'active_cases_end': b.get('active_cases_end'),
                'delta_active_cases': b.get('delta_active_cases'),
                'pct_delta_active_cases': b.get('pct_delta_active_cases'),
                'current': b.get('current')
            }
            rows.append(row)
    return rows

rows = process()
today = datetime.today().strftime('%Y-%m-%d')
current_fases = filter(lambda x: x.get('current') == 1, rows)

pd.DataFrame(rows).to_csv(f"/tmp/output/output-{today}.csv",index=False)
pd.DataFrame(rows).to_csv(f"/tmp/output/latest.csv",index=False)
pd.DataFrame(current_fases).to_csv(f"/tmp/output/current_fases.csv",index=False)
pd.DataFrame(current_fases).to_csv(f"/tmp/output/current_fases-{today}.csv",index=False)