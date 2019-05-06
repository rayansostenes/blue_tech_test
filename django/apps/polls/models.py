import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Poll(BaseModel):
    text = models.TextField(verbose_name=_('Body Text'))

    def __str__(self):
        return self.text


class Choice(BaseModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField(_('Choice Text'))
    image_url = models.TextField(_('Image URL'))

    def __str__(self):
        return self.text


class Response(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ['user', 'poll']
        ]

    def __str__(self):
        return self.user.name