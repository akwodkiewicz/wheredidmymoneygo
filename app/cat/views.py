from flask_login import login_required, current_user
from flask import redirect, url_for, flash, render_template, abort, current_app

from . import cat
from .forms import CategoryForm
from .. import db
from ..models import Category, Keyword


def check_ownership(category):
    result = False
    try:
        if current_user.id == category.user.id:
            result = True
    except Exception as e:
        pass
    finally:
        return result


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
            keyword = Keyword(word=word, category_id=category.id, enabled=True)
            db.session.add(keyword)
        db.session.commit()
        
        flash('Category added successfully!')

        return redirect(url_for('cat.categories')) 

    return render_template('cat/category.html', form=form, title='Add Category')   


@cat.route('/edit/<int:cid>', methods=['GET', 'POST'])
@login_required
def edit_category(cid):
    
    category = Category.query.get_or_404(cid)

    if check_ownership(category):
        form = CategoryForm()

        existing_keywords = set([k.word for k in category.keywords if k.enabled])
        if form.validate_on_submit():
            category.name = form.name.data

            edited_keywords = set([x.lower() for x in form.keywords.data.split()]) 

            deleted_keywords = existing_keywords - edited_keywords
            added_keywords = edited_keywords - existing_keywords


            to_disable = [Keyword.query.filter_by(word=x, category_id=category.id).one() for x in deleted_keywords]
            to_disable = [x for x in to_disable if x is not None]
            for keyword in to_disable:
                keyword.enabled = False
                db.session.add(keyword)
            
            to_enable = [Keyword.query.filter_by(word=x, category_id=category.id).first() for x in added_keywords]
            to_enable = [x for x in to_enable if x is not None]
            for keyword in to_enable:
                keyword.enabled = True
                db.session.add(keyword)

            to_add = added_keywords - set([x.word for x in to_enable])
            for word in to_add:
                keyword = Keyword(word=word, category_id=category.id, enabled=True)
                db.session.add(keyword)
            
            current_app.logger.info("TO ADD: {}".format(edited_keywords))
            current_app.logger.info("TO ENABLE: {}".format(to_enable))
            db.session.commit()
            flash('Category updated!', 'info')
            return redirect(url_for('.categories'))
            
        form.name.data = category.name
        form.keywords.data = " ".join(str(i) for i in existing_keywords)
        return render_template('cat/category.html', edit=True, form=form, title='Edit Category') 

    else:
        abort(403)



@cat.route('/delete/<int:cid>', methods=['POST'])
@login_required
def delete_category(cid):
    category = Category.query.get_or_404(cid)
    
    if check_ownership(category):
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted!', 'dark')
        return redirect(url_for('.categories'), 301)
    else:
        abort(403)