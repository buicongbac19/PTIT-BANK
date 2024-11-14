from flask import request, session, flash, render_template, redirect, url_for

from app.services.login_service import login_service


def login_controller():
    return login_service()
