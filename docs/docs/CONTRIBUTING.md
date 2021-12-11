# Contributing

Thanks for taking a look! This is primarily a personal project, but Pull Requests and Issues (questions, feature requests, etc.) are welcome. If you would like to submit a Pull Request, please open an issue first to discuss what you would like to change

## Pull Requests (PR)

### Code Development

See [./DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)

### PR Process

1. Fork the Project and Clone
2. Create a new branch (`git checkout -b feat/feature-name`)
3. Edit code; update documentation and tests; commit and push
4. Before submitting the review and pushing, make sure to run `poetry run doit`
5. Open a new Pull Request

> See the style guide for commit message format ([./STYLE_GUIDE](./STYLE_GUIDE))

If you run into any issues, please check to see if there is an open issues or open a new one

### Other PR Tips

- Link the issue with `Fixes #N` in the Pull Request body
- Please add a short summary of `why` the change was made, `what changed`, and any relevant information or screenshots

```sh
# SHA is the SHA of the commit you want to fix
git commit --fixup=SHA
# Once all the changes are approved, you can squash your commits:
git rebase --interactive --autosquash main
# Force Push
git push --force
```
