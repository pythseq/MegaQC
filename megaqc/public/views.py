# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort, json, Request
from flask_login import login_required, login_user, logout_user, current_user

from collections import OrderedDict

from megaqc.extensions import login_manager, db
from megaqc.public.forms import LoginForm
from megaqc.user.forms import RegisterForm
from megaqc.user.models import User
from megaqc.model.models import Report, PlotConfig, PlotData, PlotCategory
from megaqc.api.utils import get_samples, get_report_metadata_fields, get_sample_metadata_fields, get_report_plot_types, generate_plot
from megaqc.utils import settings, flash_errors

from sqlalchemy.sql import func, distinct
from urllib import unquote_plus

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    return render_template('public/home.html', num_samples=get_samples(count=True))

@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Log in."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('Welcome {}! You are now logged in.'.format(current_user.first_name), 'success')
            redirect_url = request.args.get('next') or url_for('public.home')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/login.html', form=form)

@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user_id = (db.session.query(func.max(User.user_id)).scalar() or 0)+1
        User.create(
            user_id=user_id,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            active=True
        )
        flash("Thanks for registering! You're now logged in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)

@blueprint.route('/plot_type/')
def choose_plot_type():
    """Choose plot type."""
    return render_template('public/plot_type.html', num_samples=get_samples(count=True))

@blueprint.route('/report_plot/')
@login_required
def report_plot_select_samples():
    # Render the template
    return render_template(
        'public/report_plot_select_samples.html',
        db = db,
        User = User,
        user_token = current_user.api_token,
        num_samples = get_samples(count=True),
        report_fields = get_report_metadata_fields(),
        sample_fields = get_sample_metadata_fields(),
        report_plot_types = get_report_plot_types()
        )


@blueprint.route('/report_plot/plot/')
@login_required
def report_plot():

    # Get the filters
    filters = []
    idx = 0
    while all(['f{}_{}'.format(idx, k) in request.values for k in ['k','t','c','v']]):
        filters.append({
            'key': request.values['f{}_k'.format(idx)],
            'type': request.values['f{}_t'.format(idx)],
            'cmp': request.values['f{}_c'.format(idx)],
            'value': request.values['f{}_v'.format(idx)]
        })
        idx += 1

    # Generate the plot
    plot_type = request.values.get('plot_type')
    samples = get_samples(filters)
    if plot_type is None:
        plot_html = '<div class="alert alert-danger">Error: No plot type supplied.</div>'
    elif len(samples) == 0:
        plot_html = '<div class="alert alert-danger">Error: No matching samples found.</div>'
    else:
        plot_html = generate_plot(plot_type, samples)

    return render_template(
        'public/report_plot.html',
        db=db,
        User=User,
        filters = filters,
        plot_html = plot_html
        )
