from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create a users table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(256))

    # 'One to many' bidirectional relationship
    accounts = db.relationship('Account', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent password from getting accessed
        """
        raise AttributeError('password is not a preadable attribute!')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


#Sets up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Account(db.Model):
    """
    Create an accounts table
    """
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 'One to many' bidirectional relationship
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic')

    def __repr__(self):
        return '<Account: {} of user {}>'.format(id, self.user.username)


class Transaction(db.Model):
    """

    Create a transactions table
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    # 'Many to one', unidirectional -- you can't get transactions from category
    category = db.relationship('Category')

    def __repr__(self):
        return '<Transaction: [{}] ${}, cat: {}, {}>'.format(id, amount, 
            self.category.name, self.account.id)


class Category(db.Model):
    """
    Create a categories table
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, index=True)

    # 'One to many', bidirectional
    keywords = db.relationship('Keyword', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category: {}>'.format(name)


class Keyword(db.Model):
    """
    Create a keywords table
    """
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Keyword: {} (cat: {})>'.format(self.word, self.category.name)