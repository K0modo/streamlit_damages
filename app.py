import streamlit as st
from pathlib import Path
import pandas as pd
import functions.graphs as gg
from functions.damage_calculations import (
    DamagesData as DD,
    prop_name_list as prop_list,
    year_list as year_list,
    month_list as month_list
)

PAGE_TITLE = "Main City | Tynan Properties"
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


@st.cache_data
def load_damages_data(file):
    return pd.read_csv(file, parse_dates=['Date'])


current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
data_file = current_dir / "data" / "main_city_surcharges_may14.csv"
dd = DD(load_damages_data(data_file))

################################################################################################################

col = st.columns((1,3,1))
with col[1]:
    st.markdown("<header style='text-align: center; font-family:verdana; font-size:30px; color:gray; "
                "border:1px solid gray; border-top-left-radius:35px; border-top-right-radius:35px; "
                "background-color:yellow'>James C. "
                "Mattingly</header>",
                unsafe_allow_html=True)

col = st.columns((1,3,1))
with col[1]:
    st.markdown("<header style='text-align: center; font-family:verdana; font-size:25px; color:gray; "
                "border:1px solid gray; border-bottom-left-radius:35px; border-bottom-right-radius:35px;"
                "background-color:yellow'><i>Tynan Litigation Support</i></header>",
                unsafe_allow_html=True)

st.markdown("")
st.markdown("")

# ROW 1
st.markdown("<h2 style='text-align: center'>Public Housing Class Action Lawsuit</h2>", unsafe_allow_html=True)
st.markdown("")

with st.expander("Background"):
    st.write("The property names and identification codes are fictitious.")
    st.write("Utilities for public housing units are limited based on the number of bedrooms in the unit.  If the "
             "tenant exceeds the utility limit (allowance) they will be charged at a fixed rate. It is the "
             "responsibility of the property manager to study utility consumption patterns regularly to keep the allowances reasonable.")
    st.write("This is a litigated case where the tenants claimed the property manager did not maintain reasonable "
             "allowances and thus sued for damages affecting over 5,000 tenants over a 4 year period.")
    st.write("Typically, public housing consists of neighborhoods (e.g. Concord, Fairfax, etc.) located throughout "
             "the city and each neighborhood has multiple buildings that contain multiple units.  Units range in "
             "size from 1 to 5 bedrooms.")

st.markdown("")
st.markdown("")

# ROW 2
col = st.columns((1, 1, 1, 1))

with col[0]:
    st.write('Total Damages')
    st.write(f'$ {dd.total_damages:,.0f}')
with col[1]:
    st.write('Customers Impacted')
    st.write(f'{dd.total_customers:,}')
with col[2]:
    st.write('Units Impacted')
    st.write(f'{dd.total_units:,}')
with col[3]:
    st.write("Months Impacted")
    st.write(f'{dd.total_months}')





# ROW 3
table = dd.population_monthly_damages()
fig = gg.make_monthly_line(table)
st.plotly_chart(fig, use_container_width=True)

# ROW 4
st.markdown("")
st.markdown("---")
st.markdown("<h2 style='text-align: center'>Property Summary of Damages</h2>", unsafe_allow_html=True)
st.markdown("")

# ROW 5
col = st.columns((.5, 8, .5))

with col[1]:
    table = dd.property_unit_damages()
    fig = gg.make_unit_strip(table)
    st.plotly_chart(fig, use_container_width=True)

# ROW 6
col = st.columns((.5, 8, .5))

with col[1]:
    st.dataframe(dd.property_summary_dataframe(),
                 column_config={
                     'Damages': st.column_config.Column(
                         width='small'
                     ),
                     'Ave Unit Damage': st.column_config.ProgressColumn(
                         format="$%.0f",
                         min_value=100,
                         max_value=400
                     ),
                     'Ave Customer Damage': st.column_config.ProgressColumn(
                         format="$%.0f",
                         min_value=0,
                         max_value=300
                     ),

                 }, hide_index=False)

# ROW 7
st.markdown("---")
st.markdown("<h3 style='text-align: center'>Population Damages</h3>", unsafe_allow_html=True)

col = st.columns((3, .05, 3))

with col[0]:
    table = dd.population_seasons()
    fig = gg.make_season_pie(table)
    st.plotly_chart(fig, use_container_width=True)

with col[2]:
    table = dd.property_bedroom_damages()
    fig = gg.make_bed_bar(table)
    st.plotly_chart(fig, use_container_width=True)

# ROW 8
st.markdown("---")
st.markdown("<h3 style='text-align: center'>Property View of Damages</h3>", unsafe_allow_html=True)

col = st.columns((2, 6))

with col[0]:
    select_property = st.selectbox("Select Property", prop_list)

# ROW 9
col = st.columns((3, 3))

with col[0]:
    table = dd.property_bed_season_tables(select_property)
    fig = gg.make_property_season_pie(table[0])
    st.plotly_chart(fig, use_container_width=True)

with col[1]:
    table = dd.property_bed_season_tables(select_property)
    fig = gg.make_property_bed_bar(table[1])
    st.plotly_chart(fig, use_container_width=True)

# ROW 10
st.markdown("---")
st.markdown("<h4 style='text-align: center'>Customize View</h4>", unsafe_allow_html=True)

# ROW 11
with st.form("property_bed_form"):
    col = st.columns((3, 3, 3))
    with col[0]:
        p_choice = st.selectbox("Select Property", prop_list)
    with col[1]:
        y_choice = st.selectbox("Select Year", year_list)
    with col[2]:
        if y_choice == 2012:
            month_list = month_list[-2:]
        if y_choice == 2016:
            month_list = month_list[:10]
        else:
            month_list = month_list
        m_choice = st.selectbox("Select Month", month_list)

    submitted = st.form_submit_button("Submit")

    if submitted:
        table = dd.select_merge_property_bed(p_choice, y_choice, m_choice)
        fig = gg.make_property_bed_chart(table)
        st.plotly_chart(fig, use_container_width=True)