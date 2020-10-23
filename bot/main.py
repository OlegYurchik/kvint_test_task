from commands import AddFixturesCommand, MakeMigrationsCommand, MigrateCommand, RunCommand
from settings import SERVICE_NAME, current_settings
from utils import parse_args, set_logging_config


COMMANDS = {
    "makemigrations": MakeMigrationsCommand,
    "migrate": MigrateCommand,
    "addfixtures": AddFixturesCommand,
    "run": RunCommand,
}


if __name__ == "__main__":
    args = parse_args(message=SERVICE_NAME, commands=COMMANDS.keys())

    if args.config is None:
        current_settings.from_env(service=SERVICE_NAME)
    else:
        current_settings.from_ini(service=SERVICE_NAME, filename=args.config)
    if all((current_settings.logging.filetype, current_settings.logging.filename)):
        set_logging_config(
            level=current_settings.logging.level,
            filetype=current_settings.logging.filetype,
            filename=current_settings.logging.filename,
        )

    command = COMMANDS[args.command](settings=current_settings)
    command.run()
