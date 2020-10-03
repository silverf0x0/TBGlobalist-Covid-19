# This script contains logic to make relation beetwen Covid deaths and the population of over 65 years old.
# Made by Raffaele Del Gatto, founder and owner of TBGlobalist (https://www.tbglobalist.com)
##
# The script is released under GNU General Public License (GPL) version 3.
# People are encouraged to use and redistribute the script for their own work. Any mention to TBGlobalist is very
# appreciated.

from pandas import DataFrame, read_csv
import pandas as pd
import matplotlib.pyplot as plt
import git
from git import Repo
import locale
import os
from datetime import date

pd.options.mode.chained_assignment = None

today = date.today()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class CovidData:
    # clone owid's covid-19-data repo if covid-19-data directory is not present (if it already exists pull last data)
    if os.path.isdir("covid-19-data"):
        our_world_in_data = git.cmd.Git('covid-19-data')
        our_world_in_data.pull()
    else:
        git.Git().clone("https://github.com/owid/covid-19-data")

    # owid dataset to explore
    owid_file = r'covid-19-data/public/data/owid-covid-data.csv'
    owid_df = pd.read_csv(owid_file)

    world_pop_file = r'world_pop_2020.csv'
    world_pop_df = pd.read_csv(world_pop_file)

    # the light owid_df takes only necessary columns of the original one
    light_owid_df = owid_df[['location', 'date', 'total_cases', 'total_deaths', 'gdp_per_capita', 'extreme_poverty']].\
        copy()
    # Add column needed to store over 65 population
    light_owid_df['over65_pop'] = 0

    # create dataframe where to store countries and their relative value, which will then be plotted via plotlib lib
    owid_to_plot_df = pd.DataFrame(columns=['continent', 'country', 'deaths_on_over65'])
    over65_age = 0

    # create dataframe where to store countries and their covid series, adjusted by deaths of over 65 years old
    # (relative value) and stringency index. The dataframe will be used to plot deaths of over 65 years old and the
    # stringency index
    stringency65_to_plot_df = pd.DataFrame(columns=['continent', 'location', 'date', 'total_cases', 'total_deaths',
                                                    'stringency_index', 'gdp_per_capita', 'new_deaths', 'over65_pop',
                                                    'new_deaths_over65'])

    # A list containing the European countries object of investigation
    european_countries = ['Austria', 'Belgium', 'Czech Republic ', 'France', 'Germany', 'Iceland', 'Italy', 'Lithuania',
                          'Norway', 'Portugal', 'Slovenia', 'Slovakia', 'Spain', 'Sweden', 'Switzerland',
                          'United Kingdom']

    # A list containing the African countries object of investigation
    african_countries = ['Burkina Faso', 'Botswana', 'Ghana', 'Nambia', 'Senegal', 'South Africa']

    # A list containing the Asian countries object of investigation
    asian_countries = ['South Korea', 'Taiwan']

    # A list containing the Oceanian countries object of investigation
    oceanian_countries = ['Australia', 'Papua New Guinea', 'New Zealand']

    # A list containing the North American countries object of investigation
    north_american_countries = ['Canada', 'Costa Rica', 'Jamaica', 'United States', 'Trinidad and Tobago']

    world_countries = european_countries+african_countries+asian_countries+oceanian_countries+north_american_countries
    world_countries.sort()

    def _agg_over65_pop(self):
        """
        The function is used to itarate over world_pop df in order to aggregate over 65 years old's population
        """
        for country in self.world_countries:
            country_df = self.world_pop_df.loc[self.world_pop_df['Country'] == country]
            for index, row in country_df.iterrows():
                if row['Age'] == '65-69' or row['Age'] == '70-74' or row['Age'] == '75-79' or row['Age'] == '80-84' or \
                        row['Age'] == '85-89' or row['Age'] == '95-99' or row['Age'] == '100+':
                    if country in self.european_countries:
                        self._population_over65_df(row['Country'], row['Age'], row['Population'], 'Europe')
                    if country in self.african_countries:
                        self._population_over65_df(row['Country'], row['Age'], row['Population'], 'Africa')
                    if country in self.asian_countries:
                        self._population_over65_df(row['Country'], row['Age'], row['Population'], 'Asia')
                    if country in self.oceanian_countries:
                        self._population_over65_df(row['Country'], row['Age'], row['Population'], 'Oceania')
                    if country in self.north_american_countries:
                        self._population_over65_df(row['Country'], row['Age'], row['Population'], 'North America')

    def _population_over65_df(self, country, age, population, continent):
        """
        The function is used to aggregate population's age for individuals of over 65 years old
        :param country: the country object of investigation
        :param age: it takes age classes from 65-69 to 100+
        :param population: float parameter containing the population of a specific age class
        """
        if age != '100+':
            self.over65_age = self.over65_age + population
        else:
            self.over65_age = self.over65_age + population
            # TO-DO:
            # Add a check to make sure that today data has been updated
            country_df = self.light_owid_df.loc[self.light_owid_df['location'] == country].iloc[-1]
            country_df['over65_pop'] = self.over65_age * 1000
            # self.final_owid_df = self.final_owid_df.append(country_df, ignore_index=True)
            self.owid_to_plot_df = self.owid_to_plot_df.append({'continent': continent, 'country': country,
                                                                'deaths_on_over65': float(country_df['total_deaths'] /
                                                                                          country_df['over65_pop']
                                                                                          )*100},
                                                               ignore_index=True)

            self.over65_age = 0
            self._tot_series_onStringency(continent, country, country_df['over65_pop'])

    def _tot_series_onStringency(self, continent, country, over65pop):
        country_df = self.light_owid_df.loc[self.light_owid_df['location'] == country]
        country_df['over65_pop'] = over65pop
        country_df['new_deaths_over65'] = round(country_df['new_deaths'] / country_df['over65_pop'] * 100, 5)
        country_df['continent'] = continent
        self.stringency65_to_plot_df = self.stringency65_to_plot_df.append(country_df, ignore_index=True)

    # Example usage below
    """
    # Initiate CovidData class
    CovidData_obj = CovidData()
    CovidData_obj._agg_over65_pop()
        
    # ************************************** European countries ****************************************** #

    Europe = CovidData_obj.owid_to_plot_df.loc[CovidData_obj.owid_to_plot_df['continent'] == 'Europe']

    # Best and worst countries
    Europe_best = Europe.sort_values(by=['deaths_on_over65'])[:5]
    Europe_worst = Europe.sort_values(by=['deaths_on_over65'], ascending=False)[:5]
    Europe_best_li = ""
    Europe_worst_li = ""
    for index, row in Europe_best.iterrows():
        over65_pop = int(CovidData.light_owid_df.loc[
                             CovidData.light_owid_df['location'] ==
                             row['country']].iloc[-1]['total_deaths'] / Europe.loc[Europe['country'] ==
                                                                                   row['country']][
                             'deaths_on_over65'] * 100)
        Europe_best_li += "<li>{} with {}% of deaths in relation to population ({}) of over 65 years old</li>". \
            format(row['country'], round(row['deaths_on_over65'], 2), over65_pop)
    for index, row in Europe_worst.iterrows():
        over65_pop = int(CovidData.light_owid_df.loc[
                             CovidData.light_owid_df['location'] ==
                             row['country']].iloc[-1]['total_deaths'] / Europe.loc[Europe['country'] ==
                                                                                   row['country']][
                             'deaths_on_over65'] * 100)
        Europe_worst_li += "<li>{} with {}% of deaths in relation to population ({}) of over 65 years old</li>". \
            format(row['country'], round(row['deaths_on_over65'], 2), over65_pop)

    # Plot bar chartover65_pop
    Europe.plot(kind='bar', x='country', figsize=(10, 10))
    plt.title("People died for Covid against population of over 65s")
    plt.ylabel("Deaths on over 65s")
    plt.xlabel("Countries")

    # Save bar chart as image
    plt.savefig('Images/Europe_over65_{}.jpg'.format(date.today()), bbox_inches='tight', dpi=150)
    """

