from datetime import datetime
from peewee import Model, DateTimeField, AutoField
from app.database import db

class TimestampModel(Model):
    id = AutoField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
    
    def to_dict(self):
        data = {}
        for field in self._meta.fields.keys():
            value = getattr(self, field)
            data[field] = value
        return data
    
    class Meta:
        database = db 