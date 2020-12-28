from app.utils import db
from sqlalchemy import exc
from datetime import datetime
from sqlalchemy.inspection import inspect
from app.repositories.base_repo import BaseRepo
from app.utils import to_camel_case, format_response_timestamp


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(
        db.DateTime(), default=datetime.now(), onupdate=datetime.now()
    )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            print("commited")
        except (exc.IntegrityError, exc.InvalidRequestError) as e:
            print("error occured===" + str(e))
            import pdb

            pdb.set_trace()

            db.session().rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize_old(self):
        s = {
            to_camel_case(column.name): getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in ["created_at", "updated_at"]
        }
        s["timestamps"] = {
            "createdAt": format_response_timestamp(self.created_at),
            "updatedAt": format_response_timestamp(self.updated_at),
        }
        return s

    def serialize(self, get_children=False):
        s = {
            to_camel_case(column.name): getattr(self, column.name)
            for column in self.__table__.columns
            if column.name
            not in ["created_at", "updated_at", "start_time", "stop_time"]
        }
        if "start_time" in self.__table__.columns:
            s[to_camel_case("start_time")] = str(self.start_time)
        if "stop_time" in self.__table__.columns:
            s[to_camel_case("stop_time")] = str(self.stop_time)
        s["timestamps"] = {
            "created_at": datetime.strftime(self.created_at, "%Y-%m-%d"),
            "updated_at": self.updated_at,
        }

        # get the related objects and serialize them
        if get_children:
            self.serialize_children_objects(s)
        return s

    def serialize_children_objects(self, s):
        """Get the model related objects and serializes them

        Args:
            s (list): serialized list object
        """
        back_refs = set(inspect(self).attrs.keys()) - set(self.__table__.columns.keys())
        for item in back_refs:
            obj = getattr(self, item)
            if isinstance(obj, list):
                list_item = [record.serialize() for record in obj]
                s[to_camel_case(item)] = list_item

    def to_dict(self, only=None, exclude=()):

        dict_obj = {}

        mapper = {
            "only": lambda obj, name, only: dict_obj.__setitem__(
                name, getattr(obj, name)
            )
            if name in only
            else False,
            "exclude": lambda obj, name, exclude: dict_obj.__setitem__(
                name, getattr(obj, name)
            )
            if name not in exclude
            else False,
        }

        if only:
            filter_func = mapper.get("only")
            predicate = only
        else:
            filter_func = mapper.get("exclude")
            predicate = exclude

        def _to_dict(obj, predicate):
            for column in obj.__table__.columns:
                filter_func(obj, column.name, predicate)

            return dict_obj

        return _to_dict(self, predicate)

    @classmethod
    def get_columns(cls):
        fields = {}

        for column in cls.__table__.columns:
            fields.__setitem__(column.name, column.type)

        return fields
