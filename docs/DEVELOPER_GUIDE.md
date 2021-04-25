# Developer Notes

## Local Development

```sh
git clone https://github.com/kyleking/dash_charts.git
cd dash_charts
poetry install

# See the available tasks
poetry run doit list

# Run the default task list (lint, auto-format, test coverage, etc.)
poetry run doit

# Make code changes and run specific tasks as needed:
poetry run doit run test
```

## Publishing

For testing, create an account on [TestPyPi](https://test.pypi.org/legacy/)

```sh
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi ...

poetry build
poetry publish --repository testpypi
# If you didn't configure a token, you will need to provide your username and password to publish
```

To publish to the real PyPi

```sh
poetry config pypi-token.pypi ...
poetry build
poetry publish

# Combine build and publish
poetry publish --build
```

> Replace "..." with the API token generated on TestPyPi/PyPi respectively

### Checklist

- [ ] Run doit tasks (test) `poetry run doit`
- [ ] Commit and push all local changes
- [ ] Increment version: `poetry run doit run cl_bump`
- [ ] Check that the README and other Markdown files are up-to-date
- [ ] Publish (see above)
