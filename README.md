# aichopen-tools
Repository containing tools used by the AI-Team

- JsonLoader: tool to load and dump json into files 

- LoggerFactory: tool to create a preconfigured logger using the singleton pattern 


## Make package publicly pip installable 
### Generate the distribution archives
```bash
python3 -m pip install --upgrade build
python3 -m build
```

### Upload to TestPyPI
Before uploading to PyPI you should verify that everything works by uploading to TestPyPI
```bash
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```
Test upload to TestPyPI
```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps aichopen-tools
```
Then refer to the usage section 

### Upload to PyPI
Once tested on TestPyPI 
```bash
python3 -m twine upload dist/*
```

## Installation
### Local 
First install
```bash
pip install .
```

If you have an existing install, and want to ensure package and dependencies are updated
```bash
pip install --upgrade .
```
or 
```bash
pip uninstall aichopen-tools
pip install .
```

### Remote
```bash
pip install aichopen-tools
```


## Usage 
    from aichopen_tools.json_loader import JsonLoader

    from aichopen_tools.logger import LoggerFactory
    

## Additional
You can find examples of issue and pull requests templates in the directory .github