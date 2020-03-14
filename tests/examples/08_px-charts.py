"""Plotly Express Examples."""

# TODO: Migrate to ex_px.py

import plotly.express as px

print(px.__version__)

tips = px.data.tips()
iris = px.data.iris()
gapminder = px.data.gapminder()
election = px.data.election()
wind = px.data.wind()
carshare = px.data.carshare()
# See explanation with: `print(px.data.iris.__doc__)`

# Possible argument combinations
px.scatter(iris, x="sepal_width", y="sepal_length", color="species", marginal_y="violin",
           marginal_x="box", trendline="ols")
px.scatter(iris, x="sepal_width", y="sepal_length", color="species", marginal_y="rug", marginal_x="histogram")
px.scatter(tips, x="total_bill", y="tip", facet_row="time", facet_col="day", color="smoker", trendline="ols",
           category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})

iris["e"] = iris["sepal_width"] / 100
px.scatter(iris, x="sepal_width", y="sepal_length", color="species", error_x="e", error_y="e")
del iris["e"]

# Animations!
px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)
px.scatter(gapminder, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country", facet_col="continent",
           log_x=True, size_max=45, range_x=[100, 100000], range_y=[25, 90])

# Example of each chart type
px.scatter_matrix(iris, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")

px.parallel_coordinates(
    iris, color="species_id",
    labels={"species_id": "Species",
            "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
            "petal_width": "Petal Width", "petal_length": "Petal Length", },
    color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2,
)

px.parallel_categories(tips, color="size", color_continuous_scale=px.colors.sequential.Inferno)

px.line(gapminder, x="year", y="lifeExp", color="continent", line_group="country", hover_name="country",
        line_shape="spline", render_mode="svg")

px.area(gapminder, x="year", y="pop", color="continent", line_group="country")

px.density_contour(iris, x="sepal_width", y="sepal_length", color="species", marginal_x="rug", marginal_y="histogram")

px.density_heatmap(iris, x="sepal_width", y="sepal_length", marginal_x="rug", marginal_y="histogram")

px.bar(tips, x="sex", y="total_bill", color="smoker", barmode="group")
px.bar(tips, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
       category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})

px.histogram(tips, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=tips.columns)
px.histogram(tips, x="sex", y="tip", histfunc="avg", color="smoker", barmode="group",
             facet_row="time", facet_col="day", category_orders={"day": ["Thur", "Fri", "Sat", "Sun"],
                                                                 "time": ["Lunch", "Dinner"]})

px.strip(tips, x="total_bill", y="time", orientation="h", color="smoker")

px.box(tips, x="day", y="total_bill", color="smoker", notched=True)

px.violin(tips, y="tip", x="smoker", color="sex", box=True, points="all", hover_data=tips.columns)

px.scatter_ternary(election, a="Joly", b="Coderre", c="Bergeron", color="winner", size="total", hover_name="district",
                   size_max=15, color_discrete_map={"Joly": "blue", "Bergeron": "green", "Coderre": "red"})

px.line_ternary(election, a="Joly", b="Coderre", c="Bergeron", color="winner", line_dash="winner")

px.scatter_polar(wind, r="value", theta="direction", color="strength", symbol="strength",
                 color_discrete_sequence=px.colors.sequential.Plotly[-2::-1])

px.line_polar(wind, r="value", theta="direction", color="strength", line_close=True,
              color_discrete_sequence=px.colors.sequential.Plotly[-2::-1])

px.bar_polar(wind, r="value", theta="direction", color="strength",
             # template="plotly_dark",
             color_discrete_sequence=px.colors.sequential.Plotly[-2::-1])

# # Maps, need Mapbox token
# px.set_mapbox_access_token(open(".mapbox_token").read())
# px.scatter_mapbox(carshare, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

# Color swatches
px.colors.qualitative.swatches()
px.colors.sequential.swatches()
px.colors.diverging.swatches()
px.colors.cyclical.swatches()
px.colors.colorbrewer.swatches()
px.colors.cmocean.swatches()
px.colors.carto.swatches()
