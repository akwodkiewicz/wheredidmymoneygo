from flask_login import login_required, current_user
from flask import redirect, url_for, flash, render_template

from . import cat
from .forms import CategoryForm
from .. import db
from ..models import Category, Keyword


@cat.route('/')
@login_required
def categories():

    categories = Category.query.filter_by(user_id=current_user.id)

    return render_template('cat/categories.html', categories=categories, title='Categories')


@cat.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():

    form = CategoryForm()
    if form.validate_on_submit():
        
        category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.flush()
        
        for word in form.keywords.data.split():
            keyword = Keyword(word=word, category_id=category.id)
            db.session.add(keyword)
        db.session.commit()
        
        flash('Category added successfully!')

        return redirect(url_for('cat.categories')) 

    return render_template('cat/category.html', form=form, title='Add Category')   
