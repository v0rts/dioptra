# Developer Guide

If you have not already, please review [CONTRIBUTING.md](CONTRIBUTING.md) for more complete information on expectations for contributions.

## Developer Set-up

### Setting up the Python virtual environment

Developers must use Python 3.11 and create a virtual environment using one of the requirements.txt files in the `requirements/` directory in order to make contributions to this project.
Ensure that you have Python 3.11 installed and that it is available in your PATH, and then identify the requirements file that you want to use:

| Filename | OS | Architecture | Tensorflow | PyTorch |
| :--- | :---: | :---: | :--- | :--- |
| linux-amd64-py3.11-requirements-dev.txt | Linux | x86-64 | ❌ | ❌ |
| linux-amd64-py3.11-requirements-dev-tensorflow.txt | Linux | x86-64 | ✅ | ❌ |
| linux-amd64-py3.11-requirements-dev-pytorch.txt | Linux | x86-64 | ❌ | ✅ |
| linux-arm64-py3.11-requirements-dev.txt | Linux | arm64 | ❌ | ❌ |
| linux-arm64-py3.11-requirements-dev-tensorflow.txt | Linux | arm64 | ✅ | ❌ |
| linux-arm64-py3.11-requirements-dev-pytorch.txt | Linux | arm64 | ❌ | ✅ |
| macos-amd64-py3.11-requirements-dev.txt | macOS | x86-64 | ❌ | ❌ |
| macos-amd64-py3.11-requirements-dev-tensorflow.txt | macOS | x86-64 | ✅ | ❌ |
| macos-amd64-py3.11-requirements-dev-pytorch.txt | macOS | x86-64 | ❌ | ✅ |
| macos-arm64-py3.11-requirements-dev.txt | macOS | arm64 | ❌ | ❌ |
| macos-arm64-py3.11-requirements-dev-tensorflow.txt | macOS | arm64 | ✅ | ❌ |
| macos-arm64-py3.11-requirements-dev-pytorch.txt | macOS | arm64 | ❌ | ✅ |
| win-amd64-py3.11-requirements-dev.txt | Windows | x86-64 | ❌ | ❌ |
| win-amd64-py3.11-requirements-dev-tensorflow.txt | Windows | x86-64 | ✅ | ❌ |
| win-amd64-py3.11-requirements-dev-pytorch.txt | Windows | x86-64 | ❌ | ✅ |

Next, use the `venv` module to create a new virtual environment:

```sh
python -m venv .venv
```

Activate the virtual environment after creating it.
To activate it on macOS/Linux:

```sh
source .venv/bin/activate
```

To activate it on Windows:

```powershell
.venv\Scripts\activate
```

Next, upgrade `pip` and install `pip-tools`:

```sh
python -m pip install --upgrade pip pip-tools
```

Finally, use `pip-sync` to install the dependencies in your chosen requirements file and install `dioptra` in development mode.
On macOS/Linux:

```sh
# Replace "linux-amd64-py3.11-requirements-dev.txt" with your chosen file
pip-sync requirements/linux-amd64-py3.11-requirements-dev.txt
```

On Windows:

```powershell
# Replace "win-amd64-py3.11-requirements-dev.txt" with your chosen file
pip-sync requirements\win-amd64-py3.11-requirements-dev.txt
```

If the requirements file you used is updated, or if you want to switch to another requirements file (you need access to the Tensorflow library, for example), just run `pip-sync` again using the appropriate filename.
It will install, upgrade, and uninstall all packages accordingly and ensure that you have a consistent environment.

### Local Development setup (without containers)
- Clone the repository at https://github.com/usnistgov/dioptra:
  ```
  git clone git@github.com:usnistgov/dioptra.git ~/dioptra/dev
  ```
  or
  ```
  git clone https://github.com/usnistgov/dioptra.git ~/dioptra/dev
  ```
- `cd ~dioptra/dev`
- `git checkout dev`
- [Install redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)
- Create a work directory for files `mkdir -p ~/dioptra/deployments/dev`
- [Create a python virtual environment](#setting-up-the-python-virtual-environment)

- The following describes commands to execute in four different terminal windows:
  1. Flask Terminal
     - Environment variables that must be set for flask:
       ```
       DIOPTRA_RESTAPI_DEV_DATABASE_URI="sqlite:////home/<username>/dioptra/deployments/dev/dioptra-dev.db"  
       DIOPTRA_RESTAPI_ENV=dev  
       DIOPTRA_RESTAPI_VERSION=v1  
       ```
       N.B.: replace <username> with your username. On some systems the home path may also be different. Verify the expansion of '~' with the `pwd` command while in the appropriate directory.

     - Activate the python environment set-up in prior steps
     - `dioptra-db autoupgrade`
     - `flask run`

  2. Frontend UI Terminal
     - Commands to get a Frontend running:
       ```bash
       cd src/fronted
       npm install
       npm run dev
       ```

  3. Redis Terminal
     - `redis-server`

  4. Dioptra Worker
     - Starting a Dioptra Worker requires the following environment variables:
       ```
       DIOPTRA_WORKER_USERNAME="dioptra-worker"  # This must be a registered user in the Dioptra app
       DIOPTRA_WORKER_PASSWORD="password"        # Must match the username's password
       DIOPTRA_API="http://localhost:5000"       # This is the default API location when you run `flask run`
       RQ_REDIS_URI="redis://localhost:6379/0"   # This is the default URI when you run `redis-server`
       MLFLOW_S3_ENDPOINT_URL="http://localhost:35000"  # If you're running a MLflow Tracking server, update this to point at it. Otherwise, this is a placeholder.
       OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES   # Macs only, needed to make the RQ worker (i.e. the Dioptra Worker) work
       ```
     - Activate the python environment set-up in prior steps (e.g. `source .venv/bin/activate`)
     - With the prior environment variables set then execute the following commands:
       ```bash
       mkdir -p ~/dioptra/deployments/dev/workdir/
       cd ~/dioptra/deployments/dev/workdir/
       dioptra-worker-v1 'Tensorflow CPU'  # Assumes 'Tensorflow CPU' is a registered Queue name
       ```
- Frontend app is available by default at http://localhost:5173 (the frontend terminal windows should also indicate the URL to use)
- Create Dioptra worker in the Frontend UI or through API. curl command for interacting with API (assuming you have the environment variables in Step iv set) is:
  ```
  curl http://localhost:5000/api/v1/users/ -X POST --data-raw "{\"username\": \"$DIOPTRA_WORKER_USERNAME\",  \"email\": \"dioptra-worker@localhost\", \"password\": \"$DIOPTRA_WORKER_PASSWORD\", \"confirmPassword\": \"$DIOPTRA_WORKER_PASSWORD\"}"
  ```
- Create 'Tensorflow CPU' Queue -- this needs to agree with the queue name used in Step iv.

### Building the documentation

This project uses Sphinx to generate the documentation published at <https://pages.nist.gov/dioptra>.
To build the documentation locally, activate your virtual environment if you haven't already and run:

```sh
python -m tox run -e web-compile,docs
```

Alternatively, you can also use `make` to do this:

```sh
make docs
```

### Reformatting code with black and isort

This project uses `black` and `isort` to automatically format Python code:
Developers are expected to run `black` and `isort` over their contributions before opening a Pull Request.
To do this, activate your virtual environment if you haven't already and run:

```sh
# Run black to reformat code
python -m tox run -e black -- src/dioptra task-plugins/dioptra_builtins tests

# Run isort to reformat import statements
python -m tox run -e isort -- src/dioptra task-plugins/dioptra_builtins tests
```

Alternatively, you can also use `make` to do this:

```sh
make beautify
```

### Checking your code with flake8 and mypy

This project uses `flake8` as a code linter and `mypy` to perform static type checking.
Developers are expected to run `flake8` and `mypy` and resolve all issues before opening a Pull Request.
To do this, activate your virtual environment if you haven't already and run:

```sh
# Lint the code
python -m tox run -e flake8

# Perform static type checking
python -m tox run -e mypy
```

Alternatively, you can also use `make` to do this:

```sh
make code-check
```

### Checking your commit message with gitlint

This project has a [commit style guide](./COMMIT_STYLE_GUIDE.md) that is enforced using the `gitlint` tool.
Developers are expected to run `gitlint` and validate their commit message before opening a Pull Request.
After committing your contribution, activate your virtual environment if you haven't already and run:

```sh
python -m tox run -e gitlint
```

Alternatively, you can also use `make` to do this:

```sh
make commit-check
```

### Running unit tests with pytest

This project stores its unit tests in the `tests/` folder and runs them using pytest.
Developers are expected to create new unit tests to validate any new features or behavior that they contribute and to verify that all unit tests pass before opening a Pull Request.
To run the unit tests, activate your virtual environment if you haven't already and run:

```sh
python -m tox run -e py311-pytest -- tests/unit
python -m tox run -e py311-cookiecutter
```

Alternatively, you can also use `make` to do this:

```sh
make tests-unit
```

### Cleanup

Run the following to clear away the project's temporary files, which includes the sentinel dotfiles that are created in `build/` when using `make`:

```sh
make clean
```
