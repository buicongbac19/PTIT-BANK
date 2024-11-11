from flask import redirect, session, render_template, flash
from app.models import Account

from app import app


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
