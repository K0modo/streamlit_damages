from datetime import datetime

import pandas as pd

prop_dict = {
    'Concord': 'con',
    'Fairfax': 'far',
    'Glouster': 'glr',
    'Helena': 'hel',
    'Miami': 'mia',
    'Wilton': 'wil'}

prop_dict_name = {value: key for key, value in prop_dict.items()}

prop_name_list = list(prop_dict.keys())
year_list = [2012, 2013, 2014, 2015, 2016]
month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def diff_month(end, start):
    return (end.year - start.year) * 12 + end.month - start.month


class DamagesData:
    def __init__(self, dataframe):
        start_date = datetime(2012, 11, 1)
        end_date = datetime(2016, 10, 1)
        self.table = dataframe
        self.total_damages = self.table.Damages.sum()
        self.total_customers = self.table.Customer_Id.nunique()
        self.total_units = self.table.Unit_Number.nunique()
        self.total_months = diff_month(end_date, start_date)

    def population_seasons(self):
        return self.table.groupby('Seasons', as_index=False)['Damages'].sum()

    def population_monthly_damages(self):
        table = self.table.groupby(['Date'], as_index=False)['Damages'].sum()
        table = table.set_index('Date')

        return table

    def property_unit_damages(self):
        return self.table.groupby(['Property_Name', 'Unit_Number'], as_index=False)['Damages'].sum()

    def property_bedroom_damages(self):
        return self.table.groupby(['Property_Name', 'Beds'], as_index=False)['Damages'].sum()

    def property_unit_count(self):
        return self.table.groupby(['Property_Name'])['Unit_Number'].nunique()

    def property_customer_count(self):
        return self.table.groupby(['Property_Name'])['Customer_Id'].nunique()

    def property_damages_total(self):
        return self.table.groupby(['Property_Name'])['Damages'].sum().astype(int)

    def property_max_unit(self):
        table = self.table.groupby(['Property_Name', 'Unit_Number'], as_index=False)['Damages'].sum()
        table = table.groupby('Property_Name')['Damages'].max().astype(int)
        return table

    def property_max_customer(self):
        table = self.table.groupby(['Property_Name', 'Customer_Id'], as_index=False)['Damages'].sum()
        table = table.groupby('Property_Name')['Damages'].max().astype(int)
        return table

    def property_summary_dataframe(self):
        property_list = prop_name_list
        table_dict = {
            'Damages': self.property_damages_total(),
            '# Units': self.property_unit_count(),
            'Unit Max': self.property_max_unit(),
            '# Customers': self.property_customer_count(),
            'Customer Max': self.property_max_customer()
        }
        table = pd.DataFrame(data=table_dict, index=property_list)
        table['Ave Unit Damage'] = table['Damages'] / table['# Units']
        table['Ave Customer Damage'] = table['Damages'] / table['# Customers']
        table['Damages'] = table['Damages'].apply(lambda x: "${:,.0f}".format(x))
        table['Unit Max'] = table['Unit Max'].apply(lambda x: "${:,.0f}".format(x))
        table['Customer Max'] = table['Customer Max'].apply(lambda x: "${:,.0f}".format(x))
        table = table.loc[:, ['Damages', 'Ave Unit Damage', 'Unit Max', 'Ave Customer Damage', 'Customer Max']]

        return table

    def property_bed_season_tables(self, choice):
        table_seasons = self.table.groupby(['Property_Name', 'Seasons'], as_index=False)['Damages'].sum()
        table_seasons = table_seasons[table_seasons['Property_Name'] == choice]
        table_beds = self.table.groupby(['Property_Name', 'Beds'], as_index=False)['Damages'].sum()
        table_beds = table_beds[table_beds['Property_Name'] == choice]

        return table_seasons, table_beds

    def select_property_bed_damages(self, p_choice, y_choice, m_choice):
        table = self.table.groupby(['Property_Name', 'Year', 'Month', 'Beds'], as_index=False)['Damages'].sum()
        table = table[table['Property_Name'] == p_choice]
        table = table[table['Year'] == y_choice]
        table = table[table['Month'] == m_choice]
        table = table.set_index('Beds')

        return table

    def select_property_bed_averages(self, p_choice):
        table = self.table[self.table['Property_Name'] == p_choice]
        table = table.groupby(['Beds'])['Damages'].mean()

        return table

    def select_merge_property_bed(self, p_choice, y_choice, m_choice):
        table_damages = self.select_property_bed_damages(p_choice, y_choice, m_choice)
        table_averages = self.select_property_bed_averages(p_choice)
        table = pd.merge(table_damages, table_averages, left_index=True, right_index=True)

        return table
