import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

def recalc():

    s = st.session_state.s
    p = st.session_state.p / 12 / 100
    n = st.session_state.n
    dt = st.session_state.dt
    tp = st.session_state.tp

    if p == 0:
        x = s / n  # размер ежемесячного платежа
    elif tp == 'аннуитетный':
        x = s * (p * (1 + p) ** n) / ((1 + p) ** n - 1)  # размер ежемесячного платежа
    else:
        x = None
        x_sm = s / n  # долговая часть

    rows = []
    sm = s  # остаток долга
    for i in range(n):
        x_prc = sm * p  # процентная часть
        if x is not None:
            x_sm = x - x_prc  # долговая часть
        dt_x = dt + relativedelta(months=i)  # дата платежа
        rows.append(
            {
                'дата платежа': dt_x.strftime('%d.%m.%Y'),
                'остаток долга': round(sm, 2),
                'ежемесячный платеж': round(x_sm + x_prc, 2),
                'процентная часть': round(x_prc, 2),
                'долговая часть': round(x_sm, 2),
                'остаток долга на конец периода': round(sm - x_sm, 2)
            }
        )
        sm = sm - x_sm
    st.session_state.df = pd.DataFrame(rows)

if 's' not in st.session_state: st.session_state.s = 300000
if 'p' not in st.session_state: st.session_state.p = 15.0
if 'n' not in st.session_state: st.session_state.n = 60
if 'dt' not in st.session_state: st.session_state.dt = date.today()
if 'tp' not in st.session_state: st.session_state.tp = 'аннуитетный'

st.title('Кредитный калькулятор')

st.number_input('Сумма кредита', min_value=1000, step=10000, format='%d', key='s', on_change=recalc)
st.number_input('Процентная ставка', min_value=0.0, step=1.0, format='%.2f', key='p', on_change=recalc)
st.number_input('Срок кредита (месяцы)', min_value=1, step=1, format='%d', key='n', on_change=recalc)
st.date_input('Дата первого платежа', format='DD.MM.YYYY', key='dt', on_change=recalc)
st.radio('Tип платежа по кредиту', options=['аннуитетный', 'дифференциальный'], horizontal=True, key='tp', on_change=recalc)

if 'df' not in st.session_state: recalc()

if st.session_state.tp == 'аннуитетный':
    x = round(st.session_state.df.loc[0, 'ежемесячный платеж'], 2)
    st.write('### Ежемесячный платеж:', x)

with st.expander('График платежей'):
    st.dataframe(st.session_state.df, hide_index=True)
