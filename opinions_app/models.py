from datetime import UTC, datetime

from . import db


def utc_now():
    """Возвращает текущее время в UTC."""
    return datetime.now(UTC)


class Opinion(db.Model):
    """Мнение о фильме."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=utc_now)
    added_by = db.Column(db.String(64))

    def to_dict(self):
        """Возвращает мнение в виде словаря."""
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            source=self.source,
            timestamp=self.timestamp,
            added_by=self.added_by,
        )

    def from_dict(self, data):
        """Заполняет только те поля, которые есть в словаре."""
        for field in ('title', 'text', 'source', 'added_by'):
            if field in data:
                setattr(self, field, data[field])
