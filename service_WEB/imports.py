# Author:  RADERMECKER Oskar, DINDIN Meryll, MISSLER Pierre-Louis
# Date:    09 July 2019
# Project: AsTeR


import os
import json
import yaml
import warnings
import requests
import numpy as np

from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging, jsonify, Response
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SubmitField, ValidationError
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mail import Mail, Message