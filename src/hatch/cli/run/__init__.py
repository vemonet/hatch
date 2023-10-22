import click


# https://github.com/cookiecutter/cookiecutter/issues/1887
def complete_scripts(ctx: click.Context, param, incomplete):
    # print("CTX", ctx)
    # print("PARAM", ctx.params['app'])
    # envs = ctx.params['app'].project.config.envs
    # envs = ctx.params
    # ctx.params.keys()

    # project.config.envs
    # template_names = get_installed_templates(ctx.params["default_config"], ctx.params["config_file"])
    # return [k for k in template_names if k.startswith(incomplete)]
    # import os
    # app.abort('Missing argument `MATRIX:ARGS...`')
    # project.config.[envs
    # click.echo('Hello World!')

    # Unfortunately click does not pass the obj to the shell_complete ctx.
    # return [k for k in ctx.obj.project.config.envs if k.startswith(incomplete)]
    # ctx.obj.project.config.envs
    return [k for k in ['test', 'lint'] if k.startswith(incomplete)]


@click.command(
    short_help='Run commands within project environment',
    context_settings={'help_option_names': [], 'ignore_unknown_options': True},
)
@click.argument('args', metavar='[ENV:]ARGS...', required=True, nargs=-1, shell_complete=complete_scripts)
@click.pass_obj
@click.pass_context
def run(ctx: click.Context, app, args):
    """
    Run commands within project environment.
    This is a convenience wrapper around the [`env run`](#hatch-env-run) command.

    If the first argument contains a colon, then the preceding component will be
    interpreted as the name of the environment to target, overriding the `-e`/`--env`
    [root option](#hatch) and the `HATCH_ENV` environment variable.

    If the environment provides matrices, then you may also provide leading arguments
    starting with a `+` or `-` to select or exclude certain variables, optionally
    followed by specific comma-separated values. For example, if you have the
    following configuration:

    === ":octicons-file-code-16: pyproject.toml"

        \b
        ```toml
        [[tool.hatch.envs.test.matrix]]
        python = ["3.9", "3.10"]
        version = ["42", "3.14", "9000"]
        ```

    === ":octicons-file-code-16: hatch.toml"

        \b
        ```toml
        [[envs.test.matrix]]
        python = ["3.9", "3.10"]
        version = ["42", "3.14", "9000"]
        ```

    then running:

    \b
    ```
    hatch run +py=3.10 -version=9000 test:pytest
    ```

    would execute `pytest` in the environments `test.py3.10-42` and `test.py3.10-3.14`.
    Note that `py` may be used as an alias for `python`.
    """
    print(ctx.obj.project.config.envs)
    if args[0] in ('-h', '--help'):
        app.display_info(ctx.get_help())
        return

    from hatch.cli.env.run import run as run_command

    command_start = 0
    included_variables = []
    excluded_variables = []
    for i, arg in enumerate(args):
        command_start = i
        if arg.startswith('+'):
            included_variables.append(arg[1:])
        elif arg.startswith('-'):
            excluded_variables.append(arg[1:])
        else:
            break
    else:
        command_start += 1

    args = args[command_start:]
    if not args:
        app.abort('Missing argument `MATRIX:ARGS...`')

    command, *args = args
    env_name, separator, command = command.rpartition(':')
    if not separator:
        env_name = app.env
    elif not env_name:
        env_name = 'system'

    ctx.invoke(
        run_command,
        args=[command, *args],
        env_names=[env_name],
        included_variable_specs=included_variables,
        excluded_variable_specs=excluded_variables,
    )
