# TODO

- Add data table examples, files: 02020X

- Add tabs, file: 0203
- Test routing: https://dash.plot.ly/urls
- Test D3/VX: https://dash.plot.ly/d3-react-components
- Check FAQs: https://dash.plot.ly/faqs
  - Maybe followup on issues with asset_url: https://dash.plot.ly/external-resources
  - Customize META/favicon: https://dash.plot.ly/external-resources
- Look into database options
  - blitzdb (alternative to nedb?): https://github.com/adewes/blitzdb
  - Syncing between GUI/Py: https://community.plot.ly/t/apache-arrow-and-dash-community-thread/7381/3
    - Perspective: https://jpmorganchase.github.io/perspective/docs/installation.html
    - Feather: https://github.com/wesm/feather
    - Arrow: https://github.com/apache/arrow/tree/master/python
- Reorganize as src/ and output/
  - Create DoIt script that downloads assets from list of URLs and creates the correct names
    - Make sure to pre-pends XX numbers to fix load order of assets. Give all custom assets `99...` to load last
  - Use cli args to pass external scripts for development with docopt (or fallback to argparse)
    - https://github.com/docopt/docopt/blob/master/examples/counted_example.py
  - *How do I make the assets folder available in PyInstaller?
  - Also script: `poetry export -f requirements.txt --without-hashes --dev`
- Checkout example charts: https://plot.ly/python/statistical-charts/
  - More examples:
    - https://gist.github.com/chriddyp/9b2b3e8a6c67697279d3724dce5dab3c
    - https://github.com/plotly/dash-recession-report-demo
    - https://github.com/plotly/dash-opioid-epidemic-demo
    - https://github.com/plotly/dash-web-trader
- Experiment with sharing state: https://dash.plot.ly/sharing-data-between-callbacks