# eReuse.org utils
Shared code used by other projects of eReuse.org.

## Installation
This library has no general dependencies, but some utilities do. To know them, go to `setup.py` file and check
`extras_require`. There you will see the specific dependencies for each of the utilities.

For example, if you want to use the `DeviceHubJsonEncoder` in `json_encoder` you don't need any dependency
as it is not shown in the `extras_require`. If you want to use `Naming` in `naming` you will need the
package `inflection`. To install it, just do `pip install -e .[usb_flash_drive]`

To keep the package minimal, only install those parts that you require:

## How to run tests
```bash
# clone repository
git clone git@github.com:eReuse/utils.git ereuse_utils
cd ereuse_utils

# prepare venv & install dependencies
export ENV_NAME='env'
python3 -m venv $ENV_NAME
source $ENV_NAME/bin/activate
pip install wheel
pip install -e .
pip install -r tests/requirements.txt

# run it
pytest --maxfail=5 tests/
```
