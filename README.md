# gaz

This is an educational endeavor into learning a bit more about ~~using Apache Arrow as a~~ data exchange methods using C++23 and Python. Some goals, which will absolutely change as I experiement and mess around with it all:

* Make Python bindings go brrrr.

I quickly realized that using Apache Arrow as an exchange format was great, but did not really buy me anything other than some additional structure to my shared data; this is great for more complex setups, but I just wanted to focus on keeping things as simple as I could, and `NumPy` + `pybind11` fits the bill. So 

<center><img src="gaz.png" width="120"></center>

## Development

Devcontainer provided; just launch a Codespace or local devcontainer!

### Build

This project uses Conan + CMake for dependency management and builds. You will need to install dependencies via Conan and then build via CMake (there are VSCode build tasks for these!):

```shell
# install dependencies
conan install . --build=missing

# install Python environment
uv sync

# load preset
cmake --preset conan-release

# build code
cmake --build --preset conan-release
```

## Examples

Just build the project, and then `uv run panel serve main.py` to launch the dashboard.
