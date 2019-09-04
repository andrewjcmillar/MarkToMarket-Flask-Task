from app import db


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120), unique=True)
    user_name = db.Column(db.String(120))
    transactions = db.relationship("Transaction", backref="transaction")

    def __init__(self, project_name, user_name):
        self.project_name = project_name
        self.user_name = user_name

    @classmethod
    def get_projects(cls, user_name):
        return [project.to_dict() for project in cls.query.filter_by(user_name=user_name).all()]

    @classmethod
    def add_project(cls, project_name, user_name):
        project = cls(project_name, user_name)
        db.session.add(project)
        db.session.commit()

    @classmethod
    def delete_project(cls, project_name):
        cls.query.filter_by(project_name=project_name).delete()
        db.session.commit()

    @classmethod
    def is_owner(cls, project_name, user_name):
        return cls.query.filter_by(project_name=project_name).first().user_name == user_name

    def to_dict(self):
        return {
            "project_name": self.project_name,
            "user_name": self.user_name
        }


class Transaction(db.Model):
    __tablename__ = 'transaction'

    def __init__(self, acquirer_name, target_id, target_name, value, project_id):
        self.acquirer_name = acquirer_name
        self.target_id = target_id
        self.target_name = target_name
        self.value = value
        self.project_id = project_id

    id = db.Column(db.Integer, primary_key=True)
    acquirer_name = db.Column(db.String(120))
    target_id = db.Column(db.Integer)
    target_name = db.Column(db.String(120))
    value = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    @classmethod
    def add_transaction(cls, acquirer_name, target_id, target_name, value, project_name):
        project_id = Project.query.filter_by(project_name=project_name).first().id
        transaction = cls(acquirer_name, target_id, target_name, value, project_id)
        db.session.add(transaction)
        db.session.commit()

    @classmethod
    def delete_transaction(cls, transaction_id):
        cls.query.filter_by(id=transaction_id).delete()
        db.session.commit()

    @classmethod
    def get_all_transactions(cls):
        return [transaction.to_dict() for transaction in cls.query.all()]

    @classmethod
    def get_all_transactions_for_project(cls, project_name):
        project_id = Project.query.filter_by(project_name=project_name).first().id
        return [transaction.to_dict() for transaction in cls.query.filter_by(project_id=project_id)]

    def to_dict(self):
        return {
            "transaction_id": self.id,
            "acquirer_name": self.acquirer_name,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "value": self.value
        }
