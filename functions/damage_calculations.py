import pandas as pd

property_dict = {
    'Concord': 'con',
    'Fairfax': 'far',
    'Glouster': 'glr',
    'Helena': 'hel',
    'Miami': 'mia',
    'Wilton': 'wil'}

property_dict_name = {value: key for key, value in property_dict.items()}

property_list = list(property_dict.keys())
year_list = [2012, 2013, 2014, 2015, 2016]
month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def diff_month(end, start):
    return (end.year - start.year) * 12 + end.month - start.month


# PD
class PropertyDamages:
    def __init__(self, dataframe):
        self.table = dataframe
        self.total_damages = self.table['Damages'].sum()
        self.total_customers = self.table['# Customers'].sum()
        self.total_units = self.table['# Units'].sum()
        self.total_months = 47

    def property_summary_table(self):
        table = self.table
        table['Ave Unit Damage'] = table['Damages'] / table['# Units']
        table['Ave Customer Damage'] = table['Damages'] / table['# Customers']
        table['Damages'] = table['Damages'].apply(lambda x: "${:,.0f}".format(x))
        table['Unit Max'] = table['Unit Max'].apply(lambda x: "${:,.0f}".format(x))
        table['Customer Max'] = table['Customer Max'].apply(lambda x: "${:,.0f}".format(x))
        table = table.loc[:, ['Damages', 'Ave Unit Damage', 'Unit Max', 'Ave Customer Damage', 'Customer Max']]

        return table


# PGD
class PropertyGroupbyDamages:
    def __init__(self, table):
        self.table = table

    def population_season_damages(self):
        return self.table.groupby('Seasons', as_index=False)['Damages'].sum()

    def population_beds_damages(self):
        return self.table.groupby('Beds', as_index=False)['Damages'].sum()

    def property_season_damages(self, choice):
        table = self.table[self.table['Property_Name'] == choice]
        table = table.groupby('Seasons', as_index=False)['Damages'].sum()
        return table

    def property_beds_damages(self, choice):
        table = self.table[self.table['Property_Name'] == choice]
        table = table.groupby('Beds', as_index=False)['Damages'].sum()
        return table

    def select_property_beds_damages(self, p_choice, y_choice, m_choice):
        table = self.table.groupby(['Property_Name', 'Year', 'Month', 'Beds'], as_index=False)['Damages'].sum()
        table = table[table['Property_Name'] == p_choice]
        table = table[table['Year'] == y_choice]
        table = table[table['Month'] == m_choice]
        table = table.set_index('Beds')

        return table

    def property_beds_monthly_average(self, p_choice):
        table = self.table[self.table['Property_Name'] == p_choice]
        table = table.groupby('Beds')['Damages'].mean()

        return table

    def select_merge_property_beds(self, p_choice, y_choice, m_choice):
        table_damages = self.select_property_beds_damages(p_choice, y_choice, m_choice)
        table_averages = self.property_beds_monthly_average(p_choice)
        table = pd.merge(table_damages, table_averages, left_index=True, right_index=True)

        return table


# MD
class MonthlyDamages:
    def __init__(self, table):
        self.table = table


# UD
class UnitDamages:
    def __init__(self, table):
        self.table = table
