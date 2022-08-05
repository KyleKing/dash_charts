## Unreleased

## 0.1.0 (2022-02-18)

## 0.1.0a1 (2022-02-06)

### Feat

- WIP experimentation with tabulator
- experiment with plotting data from calcipy release date cache

### Fix

- more fixes for nox_coverage
- properly use pd.concat
- resolve warnings from dash
- migrate to dash-bootstrap-components >=1
- drop unused matplotlib functionality
- temporarily patch the “_id” attr

### Refactor

- fix linting issues
- subset of Sourcery Refactoring
- use 'or' in place of some if/else
- add return type for generate_data
- apply sourcery refactoring
- batch add some type annotations
- experiment with Box/attr
- use self._il instead of self.ids

### New (Old)

- updates on project status
- WIP plantuml diagrams
- AppInterface and minor tweaks
- write toc to an HTML file
- split utils_dash into more specific files
- add matplotlib conversion convenience method
- refactor and add test for utils_cache
- Time Vis chart

### Change (Old)

- minor fixes to documentation
- update dash_dev dep
- implement improved SQL insert
- move into .diagrams & track png
- update image links for pdoc README
- update docs
- improve logging functionality
- drop bottleneck and update docstrings
- upgrade to latest dash_dev
- add additional tests, update docs, & fix lint
- downgrade Matplotlib 3.1 for pytest warning
- rename dash_helpers to utils_dash
- sync local changes for database & cache
- add upload image to README
- implement validation layout. Closes #2
- add username control for upload module
- add video for testing utils_static
- cleanup TODO items & fix some linting errors
- rename utils cache to json_cache
- initialize upload module example
- tests are failing for rolling chart
- refactor and cleanup of time vis and add img
- initialize new highlighted time section
- add events to time vis
- compress task list and add app_px image
- rename gantt.py to gantt_chart.py
- expand testing for dash helpers
- move source data to CSV and add to README
- cleanup and refactor
- create legendgroups to toggle projects
- sort and show Gantt tasks using Scatter @WIP
- initialize Gantt with plotly shapes @WIP
- cleanup px app
- update requirements and changelog
- set default dropdown values in child class
- add additional tests
- merge untested code from kitsu project
- merge rolling and fitted charts (inc: 0.0.5)

### Fix (Old)

- fix #3 for broken image paths to main branch
- minor bugs in datatable & drop snoop
- experiment with isort corrections
- isort and dash testing requirements
- make cache_dir configurable
- test errors and standardize log checks
- chart load errors. Resolves #1
- gantt chart image name…
- tests and add ex_gantt test
- Gantt sort and date range

## 0.0.4 (2020-05-03)

### New (Old)

- ability to create Plotly HTML from markdown
- add utils_static function tag_markdown
- improve utils_static with dominate
- refactor fitted and rolling figures
- initialize module for writing static HTML
- add slider to the rolling chart
- implement sqlite realtime demo @wip
- DataCache and general updates
- migrate to dash_dev
- remove files moved to dash_dev
- add design principles to README
- add linting to DoIt
- doit methods for placing content into README
- add example for marginal chart
- BaseDataTable class and example
- initialize “modules”
- move AppMultiPage and AppWithTabs to new file
- move examples to test/ and init dash.testing
- fitted line chart
- initialize the coordinate chart and example
- Cerberus property validation and tests
- default navbar for multipage applications
- added multi-page application base class
- @dataclass for pareto to reduce method args
- update plotly express example
- add Bootstrap example
- use external stylesheets for Bulma example
- first refactored example with Pareto chart

### Change (Old)

- update documentation
- split AppWithTabs into inline and FullScreen
- update images and dependencies
- add ex_utils_static to README
- update dash_dev for docs fixes
- use generate_data instead of _generate_data
- slightly improve annotations
- use RollingChart for SQL demo and capture gif
- set debug by CLI argument
- refactor to use dict instead of obj & use data_raw
- move some dash tutorials into tasks/package
- move px app into package
- reorganize some functions
- add filter inputs to datatable example
- move module to dash_charts
- improve datatable styling and module
- create initial module for datatable
- style sort and select in table & update docs
- refactor datatable for mutables and update ex
- add method to write sample code into README
- rename _create_traces back to create_traces()
- rename create_traces() to _create_traces()
- rename create_charts() to create_elements()
- expand tests and coverage
- minor refactor for pareto and AppBase
- add example cool hexagonal charts to WIP/
- add planned sample code (commented out) @wip
- removed alignment chart
- badges!
- remove make_colorbar and add coord_chart img
- refactor make_colorbar and remove log_fire
- use itertools and * syntax in coord chart
- refactor coordinate chart
- standardize as chart_*, data_*, id_*
- group bar placeholder
- fix formatting of raw changelog
- refactor to split run/create tasks in app
- always call Dash stylesheets from init_app
- remove dataclass for pareto & move utils_dodo
- update color scheme for Pareto
- refactor AppWithTabs and update image
- remove TODOs from README and update links
- relax version requirements in toml
- rename dash tutorial folder
- update README and pareto chart
- initialize tests and move to `plotly.express`
- update dash tutorial examples
- additional snake_case refactor
- add notes
- update rolling chart
- simplify tab example
- update documentation
- reduce complexity for map_args
- refactor utilities and initilze AppWithTabs
- update TODO annotations
- refactor the app.callback utilities
- rename examples files to be different from package files
- update data members based on Pareto changes
- experimented and semi-broke 0.0.3 tag reference
- improve documentation

### Fix (Old)

- remove mdx_gfm (doesn’t work with markdown 3)
- fix error in path for task commit_docs
- add test for ex_sqlite
- sqlite demo spawning duplicate processes
- references to app_px
- finish migration to dash_dev
- missing example image & README indentation
- set css styles to React format (not dashed)
- improve dropdown_group and add examples to px
- rendering tabs. Move create() out of init()
- update ex_px for app changes & add TODOs
- rolling & alignment charts, still work to do
- pytest class warning
- Pareto chart dataclass
- pass kwargs to __init__ and update README
- moving subdirectories to gh-pages branch
- tabs example

## 0.0.3 (2020-02-12)

### New (Old)

- show examples in documentation
- base application class
- add Tabbed Application GUI from PFE
- add annotations to rolling chart
- Add marginal charts with alignment demo
- create YearGrid and MonthGrid
- subtitles for each plot in coordinate chart
- log colors for coordinate chart
- coordinate chart
- move DoIt base utilities to separate file
- responsive Bulma example Dash app
- initApp selects assets from package
- add Bulma stylesheet to assets
- example dark theme w/ toggle

### Change (Old)

- update imports for newly split helpers file
- split helpers into charts and app utility files
- select port at CLI and more doc updates
- update requirements
- start converting to snake_case and rethinking app structure @WIP
- add optional count to Pareto bars
- proper month grid for the current year/day
- migrate to Plotly v4
- minor tweaks to alignment chart
- add customLayoutParams arg
- add plaid iframe style @wip
- add ddOpts to package and use MinGraph
- cleaned up README and TODO list @cosmetic

### Fix (Old)

- move base DoDo file into package
- cleanup lockfile and requirements
- remove github dependencies

## 0.0.2 (2019-06-17)

## 0.0.1 (2019-06-13)

### Fix (Old)

- assets paths
