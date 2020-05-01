import click
from pathlib import Path
from datetime import datetime
from freezeme.settings import load_settings
from freezeme.zipper import zip_files
from freezeme.glacier import save_in_bucket

settings_file = Path.cwd() / '.freezeme'


@click.group(invoke_without_command=True)
@click.option('--profile', default='NOTAREALDEFAULT', help='your AWS profile authorized to save to and get from s3')
@click.pass_context
def freezeme(ctx, profile):
    
    if ctx.invoked_subcommand is None:
        settings = load_settings(settings_file)
        archive_name = f'{Path.cwd().name.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        print(f'creting archive {archive_name}')
        p = Path('.')
        zip_files(p, archive_name)
        archive_path = p / archive_name
        save_in_bucket(settings, archive_path, profile)
        archive_path.unlink()


@click.command()
@click.option('--region', default='eu-central-1', help='the aws region where the bucket will be created.')
@click.pass_context
def init(ctx, region):
    settings = load_settings(settings_file, region)
    print(f'freezeme init command issued {region}')


freezeme.add_command(init)

if __name__ == "__main__":
    freezeme()
