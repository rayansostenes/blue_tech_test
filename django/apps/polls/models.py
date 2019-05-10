import uuid
from django.db import models
from django.db.models.functions import TruncHour
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Poll(BaseModel):
    """ Model that represents a Poll in the system """

    text = models.TextField(verbose_name=_('Body Text'))

    def results(self):
        """ 
        Returns a query set with all the choices for this Poll, annotates with
        a votes attr, that is a integer with the sum of all votes for this Poll 
        """
        return self.choices.annotate(votes=models.Count('vote'))

    def user_has_voted(self, user):
        """ Returns a `bool` to indicate if the user has voted on this Poll  """
        return self.vote_set.filter(user=user).exists()

    def vote(self, user, choice_id):
        return Vote.objects.create(poll=self, user=user, choice_id=choice_id)

    def __str__(self):
        return self.text


class Choice(BaseModel):
    """ This model represents all the choices available for a Poll """

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='choices',
    )
    title = models.CharField(_('Choice Text'), max_length=150)
    description = models.TextField(_('Choice Text'), null=True, blank=True)
    image_url = models.TextField(_('Image URL'), blank=True, null=True)

    def __str__(self):
        return self.title


class Vote(BaseModel):
    """ 
    This model represents the vote of each user for a Poll,
    a User can only vote one time for poll, for this reason, the properties 
    `user` and `poll` are unique together.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'poll']]

    @classmethod
    def votes_per_hour(cls, poll_id=None):
        """
        Returns the quantity of votes by hour, if poll_id is set the return
        will be filtered by poll
        """

        qs = cls.objects.annotate(
            hour=TruncHour('created_at')
        ).values('hour').annotate(votes=models.Count('id'))
        if poll_id is not None:
            qs = qs.filter(poll_id=poll_id)
        return qs

    def __str__(self):
        return 'User {} voted for {}'.format(
            self.user,
            self.choice,
        )
