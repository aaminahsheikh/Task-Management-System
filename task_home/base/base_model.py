"""All views will extend this BaseAPIView View."""
import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
