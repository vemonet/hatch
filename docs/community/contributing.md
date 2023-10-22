# Contributing

-----

The usual process to make a contribution is to:

* Check for existing related issues
* Fork the repository and create a new branch
* Make your changes
* Make sure formatting, linting and tests passes.
* Add tests if possible to cover the lines you added.
* Commit, and send a Pull Request.

## Run the tests

Run the test suite while developing:

```bash
hatch run dev
```

Run the test suite with coverage report:

```bash
hatch run cov
```

Run the extended test suite with coverage:

```bash
hatch run full
```

## Lint

Run automated formatting:

```bash
hatch run lint:fmt
```

Run full linting and type checking:

```bash
hatch run lint:all
```

## Docs

Start the documentation in development:

```bash
hatch run docs:serve
```

Build and validate the documentation website:

```bash
hatch run build-check
```
