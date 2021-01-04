import json
from pygal.maps.world import World
from pygal.style import RotateStyle as RS, LightColorizedStyle as LCS
# data for weekly cases and death in the year 2020, by countries
filename = "covid_2020_data.json"
with open(filename) as f:
    covid_data = json.load(f)
cc_cov = {}
deaths = 0
temp = "Afghanistan"
for cov_dict in covid_data:
    country_name = cov_dict["countriesAndTerritories"]

    cases = cov_dict["cases_weekly"]
    death_weekly = cov_dict["deaths_weekly"]
    code = cov_dict["geoId"].lower()
    deaths += death_weekly
    cc_cov[code] = deaths

    if country_name != temp:
        deaths = 0
    temp = country_name

# Categorising countries based on their death rate
dr1, dr2, dr3, dr4 = {}, {}, {}, {}

for cc, dr in cc_cov.items():
    if dr < 1000:
        dr1[cc] = dr
    elif dr < 10000:
        dr2[cc] = dr
    elif dr < 100000:
        dr3[cc] = dr
    else:
        dr4[cc] = dr

# Printing out the number of countries in each category
print(len(dr1), len(dr2), len(dr3), len(dr4))

wm_style = RS('#336699', base_style=LCS)
wm = World(style=wm_style)
wm.title = "Global Covid 19 deaths in 2020, by Country"
wm.add('Low(<1k)', dr1, fontsize=5)
wm.add('Moderate(<10k)', dr2)
wm.add('High(<100k)', dr3)
wm.add('Too High(>100k)', dr4)

wm.render_to_file('covid19_2020_global.svg')
