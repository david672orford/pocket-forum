from flask import Blueprint, request, session, render_template, abort, redirect

blueprint = Blueprint('submit', __name__, template_folder="templates")

