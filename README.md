# Willhaben API
This module has only tested on `https://willhaben.at`!

# Getting started:

1. Copy the contents of `config-template.ini` to a file `config.ini`
2. Set the other values in `config.ini` to fit your needs. You will need a skainet access token. If you do not have a skainet access token yet, please create one at https://auth.model.tngtech.com/.

#### uv

Install `uv`, for example as described [here](https://docs.astral.sh/uv/getting-started/installation/).

#### Python

Make sure you have a Python 3.12 version installed.

Check your installed versions with

```sh
uv python list --only-installed | grep 3.12
```

Or install with

```sh
uv python install 3.12
```

### Install project

```sh
uv sync --all-groups
```

In your IDE, set the project's Python interpreter to `</absolute/path/to/project_root>/.venv/bin/python` as described https://www.jetbrains.com/help/idea/configuring-python-sdk.html#existing-virtual-environment.



#### Extract results directly from URL
For this method you need an URL of the willhaben search you want to make. 

###### Example
This example searches for `rtx` in the `Grafikkarten` category and will show the first 1000 results.
```python
url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30"
listings = get_listings(url)
print(listings)
```