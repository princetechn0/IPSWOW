import click
from flask.cli import with_appcontext
from hash_model import CurrentApiHash
from device_model import Device
from app_setup import db


@click.command(name='create_tables')
@with_appcontext
def createTables():
    db.create_all()





