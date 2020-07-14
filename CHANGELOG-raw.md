# Changelog


## (unreleased)

### Changes

* Move source data to CSV and add to README. [Kyle King]

* Cleanup and refactor. [Kyle King]

* Create legendgroups to toggle projects. [Kyle King]

* Chg: sort and show Gantt tasks using Scatter @WIP. [Kyle King]

* Chg: initialize Gantt with plotly shapes @WIP. [Kyle King]

* Cleanup px app. [Kyle King]

* Update requirements and changelog. [Kyle King]

* Set default dropdown values in child class. [Kyle King]

* Add additional tests. [Kyle King]

* Merge untested code from kitsu project. [Kyle King]

* Merge rolling and fitted charts (inc: 0.0.5) [Kyle King]

### Fix

* Tests and add ex_gantt test. [Kyle King]

* Gantt sort and date range. [Kyle King]


## 0.0.4 (2020-05-03)

### New

* Ability to create Plotly HTML from markdown. [Kyle King]

* Add utils_static function tag_markdown. [Kyle King]

* Improve utils_static with dominate. [Kyle King]

* Refactor fitted and rolling figures. [Kyle King]

  - combined annotations function in utils_fig
  - simplified create traces for both figures

* Initialize module for writing static HTML. [Kyle King]

* Add slider to the rolling chart. [Kyle King]

* DataCache and general updates. [Kyle King]

* Migrate to dash_dev. [Kyle King]

* Remove files moved to dash_dev. [Kyle King]

* Add design principles to README. [Kyle King]

* Add linting to DoIt. [Kyle King]

* Doit methods for placing content into README. [Kyle King]

* Add example for marginal chart. [Kyle King]

* BaseDataTable class and example. [Kyle King]

* Initialize “modules” [Kyle King]

  - Need to add examples and documentation on the concept @wip

* Move AppMultiPage and AppWithTabs to new file. [Kyle King]

* Move examples to test/ and init dash.testing. [Kyle King]

* Fitted line chart. [Kyle King]

* Initialize the coordinate chart and example. [Kyle King]

* Cerberus property validation and tests. [Kyle King]

* Default navbar for multipage applications. [Kyle King]

* Added multi-page application base class. [Kyle King]

* New: @dataclass for pareto to reduce method args. [Kyle King]

* Update plotly express example. [Kyle King]

* Add Bootstrap example. [Kyle King]

* Use external stylesheets for Bulma example. [Kyle King]

* First refactored example with Pareto chart. [Kyle King]

### Changes

* Update documentation. [Kyle King]

* Split AppWithTabs into inline and FullScreen. [Kyle King]

* Update images and dependencies. [Kyle King]

* Add ex_utils_static to README. [Kyle King]

* Update dash_dev for docs fixes. [Kyle King]

* Use generate_data instead of _generate_data. [Kyle King]

* Slightly improve annotations. [Kyle King]

* Use RollingChart for SQL demo and capture gif. [Kyle King]

* Set debug by CLI argument. [Kyle King]

* Refactor to use dict instead of obj & use data_raw. [Kyle King]

* Move some dash tutorials into tasks/package. [Kyle King]

* Move px app into package. [Kyle King]

* Reorganize some functions. [Kyle King]

* Add filter inputs to datatable example. [Kyle King]

* Move module to dash_charts. [Kyle King]

* Improve datatable styling and module. [Kyle King]

* Create initial module for datatable. [Kyle King]

* Style sort and select in table & update docs. [Kyle King]

* Refactor datatable for mutables and update ex. [Kyle King]

* Add method to write sample code into README. [Kyle King]

* Rename _create_traces back to create_traces() [Kyle King]

* Rename create_traces() to _create_traces() [Kyle King]

* Rename create_charts() to create_elements() [Kyle King]

* Expand tests and coverage. [Kyle King]

* Minor refactor for pareto and AppBase. [Kyle King]

* Add example cool hexagonal charts to WIP/ [Kyle King]

  With minor modifications to [original author](https://towardsdatascience.com/interactive-basketball-data-visualizations-with-plotly-8c6916aaa59e) and [Gitlab Repository](https://gitlab.com/jphwang/online_articles)

* Removed alignment chart. [Kyle King]

* Badges! [Kyle King]

* Remove make_colorbar and add coord_chart img. [Kyle King]

* Refactor make_colorbar and remove log_fire. [Kyle King]

* Use itertools and * syntax in coord chart. [Kyle King]

* Refactor coordinate chart. [Kyle King]

* Standardize as chart_*, data_*, id_* [Kyle King]

* Group bar placeholder. [Kyle King]

* Fix formatting of raw changelog. [Kyle King]

* Refactor to split run/create tasks in app. [Kyle King]

  - Now supports production deployment with green unicorn, waitress, IIS, etc. where Flask instance needs to be a global variable

* Always call Dash stylesheets from init_app. [Kyle King]

* Remove dataclass for pareto & move utils_dodo. [Kyle King]

* Update color scheme for Pareto. [Kyle King]

* Refactor AppWithTabs and update image. [Kyle King]

* Remove TODOs from README and update links. [Kyle King]

* Relax version requirements in toml. [Kyle King]

* Rename dash tutorial folder. [Kyle King]

* Update README and pareto chart. [Kyle King]

* Initialize tests and move to `plotly.express` [Kyle King]

* Update dash tutorial examples. [Kyle King]

* Additional snake_case refactor. [Kyle King]

* Add notes. [Kyle King]

* Update rolling chart. [Kyle King]

* Simplify tab example. [Kyle King]

* Update documentation. [Kyle King]

* Reduce complexity for map_args. [Kyle King]

* Refactor utilities and initilze AppWithTabs. [Kyle King]

* Update TODO annotations. [Kyle King]

* Refactor the app.callback utilities. [Kyle King]

* Rename examples files to be different from package files. [Kyle King]

* Update data members based on Pareto changes. [Kyle King]

* Experimented and semi-broke 0.0.3 tag reference. [Kyle King]

* Improve documentation. [Kyle King]

### Fix

* Remove mdx_gfm (doesn’t work with markdown 3) [Kyle King]

* Fix error in path for task commit_docs. [Kyle King]

* Add test for ex_sqlite. [Kyle King]

* Sqlite demo spawning duplicate processes. [Kyle King]

* References to app_px. [Kyle King]

* Finish migration to dash_dev. [Kyle King]

* Missing example image & README indentation. [Kyle King]

* Set css styles to React format (not dashed) [Kyle King]

* Improve dropdown_group and add examples to px. [Kyle King]

* Rendering tabs. Move create() out of init() [Kyle King]

* Update ex_px for app changes & add TODOs. [Kyle King]

* Rolling & alignment charts, still work to do. [Kyle King]

* Pytest class warning. [Kyle King]

* Pareto chart dataclass. [Kyle King]

* Pass kwargs to __init__ and update README. [Kyle King]

* Moving subdirectories to gh-pages branch. [Kyle King]

* Tabs example. [Kyle King]


## 0.0.3 (2020-02-13)

### New

* Show examples in documentation. [Kyle King]

* Base application class. [Kyle King]

* Add Tabbed Application GUI from PFE. [Kyle King]

* Add annotations to rolling chart. [Kyle King]

* Add marginal charts with alignment demo. [Kyle King]

* Create YearGrid and MonthGrid. [Kyle King]

* Subtitles for each plot in coordinate chart. [Kyle King]

* Log colors for coordinate chart. [Kyle King]

* Coordinate chart. [Kyle King]

* Move DoIt base utilities to separate file. [Kyle King]

* Responsive Bulma example Dash app. [Kyle King]

* InitApp selects assets from package. [Kyle King]

* Add Bulma stylesheet to assets. [Kyle King]

  Added `limitCat` argument to ParetoChart()

* Example dark theme w/ toggle. [Kyle King]

  Fixed release tags in history

### Changes

* Update imports for newly split helpers file. [Kyle King]

* Split helpers into charts and app utility files. [Kyle King]

* Select port at CLI and more doc updates. [Kyle King]

* Update requirements. [Kyle King]

* Chg: start converting to snake_case and rethinking app structure @WIP. [Kyle King]

* Add optional count to Pareto bars. [Kyle King]

* Proper month grid for the current year/day. [Kyle King]

* Migrate to Plotly v4. [Kyle King]

* Minor tweaks to alignment chart. [Kyle King]

* Add customLayoutParams arg. [Kyle King]

* Add ddOpts to package and use MinGraph. [Kyle King]

### Fix

* Move base DoDo file into package. [Kyle King]

* Cleanup lockfile and requirements. [Kyle King]

* Remove github dependencies. [Kyle King]

### Other

* Change: implement OOP for examples. [Kyle King]

* Add: CHANGELOG (0.0.3) [Kyle King]

* Refac: use class to manage app variables. [Kyle King]

* Add: additional px chart types. [Kyle King]

* Add: context and polar/ternary charts. [Kyle King]

* Add: tabbed px demo. [Kyle King]

* Add: examples with plotly express. [Kyle King]

* Mv: reorganize tutorials into separate dir. [Kyle King]

* Add: tools for pushing documentation. [Kyle King]

* Init: pdoc documentation. [Kyle King]


## 0.0.2 (2019-06-18)

### Other

* Refac: cleanup README. [Kyle King]

* Add: Pareto Chart. [Kyle King]

* Add: rolling chart. [Kyle King]

* Add: alignment chart and base custom chart class. [Kyle King]

* Mv: reorganized to be a Python module. [Kyle King]

  (Archived initial project to `archive/dash-helloworld` branch)

* Mv: rename and implement relative imports. [Kyle King]

* WIP: add bottleneck and refactor. [Kyle King]

* Add: more interesting sample data and best fit. [Kyle King]

* Add: demo SQLite backend write/dashboard read. [Kyle King]

* Refac: use datatables backend example. [Kyle King]


## 0.0.1 (2019-06-14)

### Fix

* Assets paths. [Kyle King]

### Other

* Mv: reorganize into subdirectory. [Kyle King]

* Add: Pareto chart example. [Kyle King]

* Init: Dash Tabs Demo and Distortion Chart. [Kyle King]

* Inc: minimum requirements. [Kyle King]

* Add: three Dash example datatable pages. [Kyle King]

* Add: example with (most) HTML components. [Kyle King]

* Refac: use local assets instead of external links. [Kyle King]

* Init: first example following chapter 02. [Kyle King]

* Initial commit. [Kyle King]


