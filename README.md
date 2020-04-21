# ps2-analysis [WIP]

*ps2-analysis* is a library written in Python >= 3.8 that uses the [ps2-census](https://github.com/spascou/ps2-census)
Daybreak Planetside 2 Census API client to get data and then analyses it.

   * [ps2-analysis](#ps2-analysis)
      * [Setup](#setup)

## Setup

- Clone this repository
- Setup a Python >= 3.8 virtual environment
- Install [poetry](https://github.com/python-poetry/poetry)
- Install dependencies with `poetry install`
- Run tests with `pytest`
- Update dependencies with `poetry update`

- Add your Census API service ID to the `CENSUS_SERVICE_ID` environment variable
- Create two folders inside the `examples` of the cloned repository: `datafiles` and `plots`

- Run python scripts in examples

It will update the `examples/datafiles/weapons.ndjson` file from the Census API, then parse the data
and generate whatever output the example script calls for.

Plots are interactive and generated with [altair](https://github.com/altair-viz/altair), so they need to be opened in
a browser.

If `examples/datafiles/weapons.ndjson` already exists, next execution will simply read it instead of
updating from the API. Delete it to force the update, if so wished.
