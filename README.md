# winipedia-utils


## Project Setup
When you start a new project you can use winipedia-utils to set up the project.
It is assumed that you use git and poetry for your project.
It is assumed that the root folder (cwd) has the same name as the repository and follows the naming convention of smth-smth with hyphens.

Lets say your project is called my-project. Then you would do the following:

```bash
poetry init or poetry new
poetry add winipedia-utils
poetry run winipedia-utils create-root
```

This will create the following structure (with __init__.py files):

```bash
my-project
├── my_project
│   ├── dev
│   │   ├── artifacts
│   │   │   └── builder
│   │   │   │   ├── builder.py
│   │   ├── cli
│   │   │   ├── cli.py
│   │   │   ├── subcommands.py
│   │   ├── configs
│   │   │   ├── configs.py
├── tests
│   ├── base
│   │   ├── fixtures
│   │   ├── utils
│   │   │   ├── utils.py
│   └── test_my_project
│   │   ├── __init__.py
│   │   └── test_builder.py
│   └── conftest.py
│   └── test_zero.py
│   
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── experiment.py
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
└── ...
```