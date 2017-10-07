from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from . import tran
from .forms import TransactionForm
from .. import db
from ..models import Transaction, Account, Category

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

        flash('Transaction added successfully', 'success')
        return redirect(url_for('tran.transactions'))

    return render_template('tran/transaction.html', form=form, title="Add Transaction")

