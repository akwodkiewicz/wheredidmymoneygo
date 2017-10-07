from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from . import tran
from .forms import TransactionForm
from .. import db
from ..models import Transaction, Account, Category


def check_ownership(transaction):
    result = False
    try:
        if transaction.account.user.id == current_user.id:
            result = True
    except Exception as e:
        raise e
    finally:
        return result

@tran.route('/')
@login_required
def transactions():
    """
    Shows all transactions in one account
    """
    account = current_user.accounts.first()
    if account is None:
        transactions = []
    else:
        transactions = account.transactions
    return render_template('tran/transactions.html', title="Transactions",
                                                    transactions=transactions)


@tran.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """
    Adds a transaction
    """
    form = TransactionForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id)]
    
    if form.validate_on_submit():

        amount = form.amount.data
        if form.ttype.data == 'out':
            amount *= -1

        account = current_user.accounts.first()

        t = Transaction(amount=amount, description=form.description.data,
                        date=form.date.data, category_id=form.category.data, 
                        account_id=account.id)
        db.session.add(t)
        db.session.commit()

        flash('Transaction added successfully', 'info')
        return redirect(url_for('tran.transactions'))

    return render_template('tran/transaction.html', form=form, title="Add Transaction")


@tran.route('/edit/<int:tid>', methods=['GET', 'POST'])
@login_required
def edit_transaction(tid):
    transaction = Transaction.query.get_or_404(tid)
    
    if check_ownership(transaction):
        form = TransactionForm(obj=transaction)
        form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id)]

        if form.validate_on_submit():

            transaction.amount = form.amount.data
            if form.ttype.data == 'out':
                transaction.amount *= -1
            transaction.description=form.description.data
            transaction.date=form.date.data
            transaction.category_id=form.category.data

            db.session.commit()
            flash('Transaction edited!', 'info')

            return redirect(url_for('.transactions')) 

        if transaction.amount > 0:
            form.ttype.data = 'in'
        else:
            form.amount.data *= (-1)
            form.ttype.data = 'out'

        return render_template('tran/transaction.html', form=form, title='Edit Transaction')
    else:
        abort(403)


@tran.route('/delete/<int:tid>', methods=['POST'])
@login_required
def delete_transaction(tid):
    transaction = Transaction.query.get_or_404(tid)
    
    if check_ownership(transaction):
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted!', 'dark')
        return redirect(url_for('.transactions'), 301)
    else:
        abort(403)