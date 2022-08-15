import os
from flask import Flask, render_template,request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from sqlalchemy import ForeignKey

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:passer@localhost:5432/fyyurdb'
