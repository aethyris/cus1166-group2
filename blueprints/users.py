from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from models import User, db, Filter, Recipe, Ingredient
from forms import LoginForm, RegistrationForm, UserInfoForm, FilterForm
from datetime import datetime

users = Blueprint('users', __name__, template_folder="templates")

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home_page.index'))
    return render_template('login.html', form=form)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home_page.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page.index'))


@users.route('/user/<username>')
def view_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@users.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    info_form = UserInfoForm(obj=current_user)
    filter_form = FilterForm(obj=current_user.filters)
    if info_form.validate_on_submit():
        current_user.username = info_form.username.data
        current_user.description = info_form.description.data
        current_user.avatar = info_form.avatar.data
        current_user.email = info_form.email.data
        db.session.commit()
        return redirect(url_for('users.settings'))
    elif filter_form.validate_on_submit():
        current_user.filters.price_min = filter_form.price_min.data
        current_user.filters.price_max = filter_form.price_max.data
        current_user.filters.calorie_min = filter_form.calorie_min.data
        current_user.filters.calorie_max = filter_form.calorie_max.data
        current_user.filters.meal_type = filter_form.meal_type.data
        current_user.filters.meal_style = filter_form.meal_style.data
        current_user.filters.dietary_preferences = filter_form.dietary_preferences.data
        current_user.filters.cooking_time_min = filter_form.cooking_time_min.data
        current_user.filters.cooking_time_max = filter_form.cooking_time_max.data
        db.session.commit()
        return redirect(url_for('users.settings'))
    return render_template('settings.html', user_info=current_user, info_form=info_form)

@users.route('/create_recipe', methods=["GET", "POST"])
def addRecipe():
    if request.form:
        recipe = Recipe(recipe_title=request.form.get("recipe_title")), \
                 Recipe(recipe_description=request.form.get("recipe_description")), \
                 Recipe(recipe_picture=request.form.get("recipe_upload")), \
                 Recipe(recipe_cooking_time=request.form.get("recipe_cooking_time")),\
                 Recipe(recipe_calorie_count=request.form.get("recipe_calories"))
        db.session.add(recipe)
        db.session.commit()

        return render_template(settings.html, user_info=current_user)
