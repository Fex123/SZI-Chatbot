from flask.json.provider import JSONProvider
from datetime import datetime
from bson import ObjectId
import json

"""
CustomJSONProvider class
Custom JSON Provider to handle datetime and ObjectId serialization
"""
class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=self._default)
    
    def loads(self, s, **kwargs):
        return json.loads(s)
    
    def _default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f'Object of type {type(obj)} is not JSON serializable')
