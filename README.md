# ps2-analysis [WORK IN PROGRESS]

*ps2-analysis* is a library written in Python >= 3.8 that fetches data from the
Daybreak Planetside 2 Census API and eases advanced analysis.

It uses its sister project, the [ps2-census](https://github.com/spascou/ps2-census) client
whose objective is simply to handle data retrieval from the Census API. Further parsing
and exploitation is performed here in *ps2-analysis*.

   * [ps2-analysis](#ps2-analysis)
      * [Examples](#examples)
      * [Development](#development)
        * [Environment](#environment)

*Features*:
- Currently supports infantry weapons data
- Downloads datasets from the API and stores them locally as *ndjson* files
- Parses data and generates class objects suitable for further processing
- Generates *vega-lite* charts using [Altair](https://altair-viz.github.io/)

## Installation
```sh
pip install ps2-analysis
```

## Examples

Examples are available in the `examples` folder:
- `discover.py`: updates the infantry weapons datafile and outputs all different (nested) key paths as well as associated set of values encountered within the whole dataset; example output in `discover.json`
- `generate_infantry_weapons.py`: no output; simply an example of `InfantryWeapon` objects generation
- `fire_simulation_plot.py`: generates a fire simulation plot for the TRAC-5 TR carbine, 100 runs of 10 shots
- `ttk_to_mhd_plot.py`: generates a plot of time to kill at 15meters to mean horizontal deviation for all SMGs

## Development

### Environment

In order to develop *ps2-analysis*:
- Setup a virtual environment with python 3.8
- Install [poetry](https://github.com/python-poetry/poetry)
- Install dependencies with `poetry install`
- Run tests with `pytest`
- Update dependencies with `poetry update`

To run the examples in the `examples` folder:
- Add your Census API service ID to the `CENSUS_SERVICE_ID` environment variable
- Create two folders inside the `examples` folder of the cloned repository: `datafiles` and `plots`
- Run the scripts and check the outputs
