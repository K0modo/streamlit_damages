import streamlit as st
from pathlib import Path
import pandas as pd
import functions.graphs as gg
from functions.damage_calculations import (
    DamagesData as DD,
    DamagesProperty as DP,
    UnitDamages as UD,
    MonthlyDamages as MD,
    PropertyGroupbyDamages as PGD,
    property_list as property_list,
    year_list as year_list,
    month_list as month_list
)

PAGE_TITLE = "Main City | Tynan Properties"
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


@st.cache_data
def load_damages_data(file):
    return pd.read_csv(file, parse_dates=['Date'])


@st.cache_data
def load_property_damages(file):
    return pd.read_csv(file, index_col=0)


@st.cache_data
def load_monthly_damages(file):
    return pd.read_csv(file, index_col=0)


@st.cache_data
def load_unit_damages(file):
    return pd.read_csv(file)


@st.cache_data
def load_property_groupby_table(file):
    return pd.read_csv(file)


current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

master_file = current_dir / "data" / "master_may14.csv"
m_df = DD(load_damages_data(master_file))

property_file = current_dir / "data" / "property_summary_table.csv"
property_table = DP(load_property_damages(property_file))

monthly_damage_file = current_dir / "data" / "monthly_damages.csv"
month_table = MD(load_monthly_damages(monthly_damage_file))

unit_damages_file = current_dir / "data" / "unit_damages.csv"
unit_table = UD(load_unit_damages(unit_damages_file))

property_groupby_file = current_dir / "data" / "property_groupby_all.csv"
property_groupby_table = PGD(load_property_groupby_table(property_groupby_file))

################################################################################################################

col = st.columns((1,3,1))
with col[1]:
    st.markdown("<header style='text-align: center; font-family:verdana; font-size:28px; color:gray; "
                "border:1px solid gray; border-top-left-radius:35px; border-top-right-radius:35px; "
                "background-color:yellow'>James C. "
                "Mattingly</header>",
                unsafe_allow_html=True)

col = st.columns((1,3,1))
with col[1]:
    st.markdown("<header style='text-align: center; font-family:verdana; font-size:28px; color:gray; "
                "border:1px solid gray; border-bottom-left-radius:35px; border-bottom-right-radius:35px;"
                "background-color:yellow'>Tynan Litigation Support</header>",
                unsafe_allow_html=True)

st.markdown("")
st.markdown("")

# ROW 1
st.markdown("<h2 style='text-align: center'>Public Housing Class Action Lawsuit</h2>", unsafe_allow_html=True)
st.markdown("")

with st.expander("Project Background"):
    st.write("Consumption of utilities for public housing units are limited based on the number of bedrooms in the "
             "unit.  If the tenant exceeds the utility limit (allowance) they will be charged at a fixed rate. It is "
             "the responsibility of the property manager to study utility consumption patterns regularly to keep the"
             " allowances reasonable.")
    st.write("This is a litigated case where the tenants claimed the property manager did not maintain reasonable "
             "allowances and thus sued for damages affecting over 5,000 tenants over a 4 year period.")
    st.write("Typically, public housing consists of neighborhoods (e.g. Concord, Fairfax, etc.) located throughout "
             "the city and each neighborhood has multiple buildings that contain multiple units.  Units range in "
             "size from 1 to 5 bedrooms.")
    st.write("The property names and identification codes are fictitious.")

st.markdown("")
st.markdown("")

# ROW 2
col = st.columns((1, 1, 1, 1))

with col[0]:
    st.write('Total Damages')
    st.write(f'$ {property_table.total_damages:,.0f}')
with col[1]:
    st.write('Customers Impacted')
    st.write(f'{property_table.total_customers:,}')
with col[2]:
    st.write('Units Impacted')
    st.write(f'{property_table.total_units:,}')
with col[3]:
    st.write("Months Impacted")
    st.write(f'{property_table.total_months}')


# ROW 3
table = month_table.table
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
    table = unit_table.table
    fig = gg.make_unit_strip(table)
    st.plotly_chart(fig, use_container_width=True)

# ROW 6
col = st.columns((.5, 8, .5))

with col[1]:
    st.dataframe(property_table.property_summary_table(),
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
    table = property_groupby_table.population_season_damages()
    fig = gg.make_season_pie(table)
    st.plotly_chart(fig, use_container_width=True)

with col[2]:
    table = property_groupby_table.population_beds_damages()
    fig = gg.make_bed_bar(table)
    st.plotly_chart(fig, use_container_width=True)

# ROW 8
st.markdown("---")
st.markdown("<h3 style='text-align: center'>Property View of Damages</h3>", unsafe_allow_html=True)

col = st.columns((2, 6))

with col[0]:
    select_property = st.selectbox("Select Property", property_list)

# ROW 9
col = st.columns((3, 3))

with col[0]:
    table = property_groupby_table.property_season_damages(select_property)
    fig = gg.make_property_season_pie(table)
    st.plotly_chart(fig, use_container_width=True)

with col[1]:
    table = property_groupby_table.property_bed_damages(select_property)
    fig = gg.make_property_bed_bar(table)
    st.plotly_chart(fig, use_container_width=True)

# ROW 10
st.markdown("---")
st.markdown("<h4 style='text-align: center'>Customize View</h4>", unsafe_allow_html=True)

# ROW 11
with st.form("property_bed_form"):
    col = st.columns((3, 3, 3))
    with col[0]:
        p_choice = st.selectbox("Select Property", property_list)
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
        table = property_groupby_table.select_merge_property_bed(p_choice, y_choice, m_choice)
        fig = gg.make_property_bed_chart(table)
        st.plotly_chart(fig, use_container_width=True)
