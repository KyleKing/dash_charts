"""Plotly Express Examples."""

# TODO: Migrate this sample code to ex_app_px.py

import plotly.express as px

print(px.__version__)

tips = px.data.tips()
#      total_bill   tip     sex smoker   day    time  size
# 0         16.99  1.01  Female     No   Sun  Dinner     2
# 1         10.34  1.66    Male     No   Sun  Dinner     3
# ..          ...   ...     ...    ...   ...     ...   ...
# 242       17.82  1.75    Male     No   Sat  Dinner     2
# 243       18.78  3.00  Female     No  Thur  Dinner     2

# [244 rows x 7 columns]

iris = px.data.iris()
#      sepal_length  sepal_width  petal_length  petal_width    species  species_id
# 0             5.1          3.5           1.4          0.2     setosa           1
# 1             4.9          3.0           1.4          0.2     setosa           1
# ..            ...          ...           ...          ...        ...         ...
# 148           6.2          3.4           5.4          2.3  virginica           3
# 149           5.9          3.0           5.1          1.8  virginica           3

# [150 rows x 6 columns]

gapminder = px.data.gapminder()
#           country continent  year  lifeExp       pop   gdpPercap iso_alpha  iso_num
# 0     Afghanistan      Asia  1952   28.801   8425333  779.445314       AFG        4
# 1     Afghanistan      Asia  1957   30.332   9240934  820.853030       AFG        4
# ...           ...       ...   ...      ...       ...         ...       ...      ...
# 1702     Zimbabwe    Africa  2002   39.989  11926563  672.038623       ZWE      716
# 1703     Zimbabwe    Africa  2007   43.487  12311143  469.709298       ZWE      716

# [1704 rows x 8 columns]

election = px.data.election()
#                     district  Coderre  Bergeron  Joly  total    winner     result  district_id
# 0         101-Bois-de-Liesse     2481      1829  3024   7334      Joly  plurality          101
# 1      102-Cap-Saint-Jacques     2525      1163  2675   6363      Joly  plurality          102
# ...                      ...      ...       ...   ...    ...       ...        ...          ...
# 56        93-Robert-Bourassa      446       465   419   1330  Bergeron  plurality           93
# 57           94-Jeanne-Sauvé      491       698   489   1678  Bergeron  plurality           94
# # [58 rows x 8 columns]

wind = px.data.wind()
#     direction strength  frequency
# 0           N      0-1        0.5
# 1         NNE      0-1        0.6
# ..        ...      ...        ...
# 126        NW       6+        1.5
# 127       NNW       6+        0.2

# [128 rows x 3 columns]

carshare = px.data.carshare()
#      centroid_lat  centroid_lon    car_hours  peak_hour
# 0       45.471549    -73.588684  1772.750000          2
# 1       45.543865    -73.562456   986.333333         23
# ..            ...           ...          ...        ...
# 247     45.521199    -73.581789  1044.833333         17
# 248     45.532564    -73.567535   694.916667          5

# [249 rows x 4 columns]

# See explanation with: `print(px.data.iris.__doc__)`

# Possible argument combinations
px.scatter(iris, x='sepal_width', y='sepal_length', color='species', marginal_y='violin',
           marginal_x='box', trendline='ols')
px.scatter(iris, x='sepal_width', y='sepal_length', color='species', marginal_y='rug', marginal_x='histogram')
px.scatter(tips, x='total_bill', y='tip', facet_row='time', facet_col='day', color='smoker', trendline='ols',
           category_orders={'day': ['Thur', 'Fri', 'Sat', 'Sun'], 'time': ['Lunch', 'Dinner']})

iris['e'] = iris['sepal_width'] / 100
px.scatter(iris, x='sepal_width', y='sepal_length', color='species', error_x='e', error_y='e')
del iris['e']

# Animations!
px.scatter(gapminder.query('year==2007'), x='gdpPercap', y='lifeExp', size='pop', color='continent',
           hover_name='country', log_x=True, size_max=60)
px.scatter(gapminder, x='gdpPercap', y='lifeExp', animation_frame='year', animation_group='country',
           size='pop', color='continent', hover_name='country', facet_col='continent',
           log_x=True, size_max=45, range_x=[100, 100000], range_y=[25, 90])

# Example of each chart type
px.scatter_matrix(iris, dimensions=['sepal_width', 'sepal_length', 'petal_width', 'petal_length'], color='species')

px.parallel_coordinates(
    iris, color='species_id',
    labels={'species_id': 'Species',
            'sepal_width': 'Sepal Width', 'sepal_length': 'Sepal Length',
            'petal_width': 'Petal Width', 'petal_length': 'Petal Length'},
    color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2,
)

px.parallel_categories(tips, color='size', color_continuous_scale=px.colors.sequential.Inferno)

px.line(gapminder, x='year', y='lifeExp', color='continent', line_group='country', hover_name='country',
        line_shape='spline', render_mode='svg')

px.area(gapminder, x='year', y='pop', color='continent', line_group='country')

px.density_contour(iris, x='sepal_width', y='sepal_length', color='species', marginal_x='rug', marginal_y='histogram')

px.density_heatmap(iris, x='sepal_width', y='sepal_length', marginal_x='rug', marginal_y='histogram')

px.bar(tips, x='sex', y='total_bill', color='smoker', barmode='group')
px.bar(tips, x='sex', y='total_bill', color='smoker', barmode='group', facet_row='time', facet_col='day',
       category_orders={'day': ['Thur', 'Fri', 'Sat', 'Sun'], 'time': ['Lunch', 'Dinner']})

px.histogram(tips, x='total_bill', y='tip', color='sex', marginal='rug', hover_data=tips.columns)
px.histogram(tips, x='sex', y='tip', histfunc='avg', color='smoker', barmode='group',
             facet_row='time', facet_col='day', category_orders={'day': ['Thur', 'Fri', 'Sat', 'Sun'],
                                                                 'time': ['Lunch', 'Dinner']})

px.strip(tips, x='total_bill', y='time', orientation='h', color='smoker')

px.box(tips, x='day', y='total_bill', color='smoker', notched=True)

px.violin(tips, y='tip', x='smoker', color='sex', box=True, points='all', hover_data=tips.columns)

px.scatter_ternary(election, a='Joly', b='Coderre', c='Bergeron', color='winner', size='total', hover_name='district',
                   size_max=15, color_discrete_map={'Joly': 'blue', 'Bergeron': 'green', 'Coderre': 'red'})

px.line_ternary(election, a='Joly', b='Coderre', c='Bergeron', color='winner', line_dash='winner')

px.scatter_polar(wind, r='value', theta='direction', color='strength', symbol='strength',
                 color_discrete_sequence=px.colors.sequential.Plotly[-2::-1])

px.line_polar(wind, r='value', theta='direction', color='strength', line_close=True,
              color_discrete_sequence=px.colors.sequential.Plotly[-2::-1])

px.bar_polar(wind, r='value', theta='direction', color='strength',
             # template='plotly_dark',
             color_discrete_sequence=px.colors.sequential.Plotly[-2::-1])

# # Maps, need Mapbox token
# px.set_mapbox_access_token(open('.mapbox_token').read())
# px.scatter_mapbox(carshare, lat='centroid_lat', lon='centroid_lon', color='peak_hour', size='car_hours',
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

# Color swatches
px.colors.qualitative.swatches()
px.colors.sequential.swatches()
px.colors.diverging.swatches()
px.colors.cyclical.swatches()
px.colors.colorbrewer.swatches()
px.colors.cmocean.swatches()
px.colors.carto.swatches()
