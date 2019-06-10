# TODO

# TODO: Pareto Snippet with SQL
#  See: https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/
# df = pd.read_sql_query('SELECT ComplaintType, COUNT(*) as `num_complaints`, Agency '
#                        'FROM data '
#                        'GROUP BY `ComplaintType` '
#                        'ORDER BY -num_complaints', disk_engine)

- Test routing: https://dash.plot.ly/urls
- Test D3/VX: https://dash.plot.ly/d3-react-components
- Check FAQs: https://dash.plot.ly/faqs
  - Maybe followup on issues with asset_url: https://dash.plot.ly/external-resources
  - Customize META/favicon: https://dash.plot.ly/external-resources
- Look into database options
  - See SQLite. Example above ^^
  - blitzdb (alternative to nedb?): https://github.com/adewes/blitzdb
  - Syncing between GUI/Py: https://community.plot.ly/t/apache-arrow-and-dash-community-thread/7381/3
    - Perspective: https://jpmorganchase.github.io/perspective/docs/installation.html
    - Feather: https://github.com/wesm/feather
    - Arrow: https://github.com/apache/arrow/tree/master/python
- Checkout the v2 Table Filtering in Dash 0.43
- Checkout example charts: https://plot.ly/python/statistical-charts/
  - More examples:
    - https://gist.github.com/chriddyp/9b2b3e8a6c67697279d3724dce5dab3c
    - https://github.com/plotly/dash-recession-report-demo
    - https://github.com/plotly/dash-opioid-epidemic-demo
    - https://github.com/plotly/dash-web-trader
- Experiment with sharing state: https://dash.plot.ly/sharing-data-between-callbacks
