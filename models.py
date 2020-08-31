from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User Model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    dashboards = db.relationship("Dashboard", backref="owner")
    feeds = db.relationship("Feed", backref="owner")
    tokens = db.relationship("Token", backref="owner")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        """return dict representation"""
        return {
            "id": self.id,
            "username": self.username,
            "created": self.created,
            "dashboards": [dashboard.to_dict() for dashboard in self.dashboards],
            "feeds": [feed.to_dict() for feed in self.feeds],
        }


class Token(db.Model):
    """
    Token Model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    secret = db.Column(db.String, nullable=False, unique=True)
    allowed_feeds = db.relationship("Feed", backref="token")
    user_scope = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False)
    last_used = db.Column(db.DateTime, nullable=True, default=None)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        """returns dict representation"""
        return {
            "id": self.id,
            "name": self.name,
            "secret": self.secret,
            "allowed_feeds": [feed.id for feed in self.allowed_feeds],
            "created": self.created,
            "last_used": self.last_used,
            "owner": self.owner,
        }


class Dashboard(db.Model):
    """
    Dashboard Model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    feeds = db.relationship("Feed", backref="dashboard")

    def set_name(self, name):
        """set name and slug"""
        self.name = name
        self.slug = slugify(name)

    def to_dict(self):
        """return dict representation"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "created": self.created,
            "owner": self.owner.username,
            "feeds": [feed.to_dict() for feed in self.feeds],
        }


class Feed(db.Model):
    """
    Feed Model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    kind = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboard.id"), nullable=False)
    data = db.relationship("Data", backref="feed")
    token_id = db.Column(db.Integer, db.ForeignKey("token.id"))

    def to_dict(self):
        """return dict representation"""

        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "kind": self.kind,
            "created": self.created,
            "owner": self.owner,
            "dashboard": self.dashboard,
            "data": [data.to_dict() for data in self.data],
        }


class Data(db.Model):
    """
    Data Model
    """

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey("feed.id"), nullable=False)

    def to_dict(self):
        """return dict representation"""

        return {
            "id": self.id,
            "value": self.value,
            "created": self.created,
            "feed": self.dashboard,
        }
