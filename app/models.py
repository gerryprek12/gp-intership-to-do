from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

PRIORITY_OPTION_LOW = 3
PRIORITY_OPTION_MEDIUM = 2
PRIORITY_OPTION_HIGH = 1

PRIORITY_OPTIONS = (
    (PRIORITY_OPTION_LOW, 'Low'),
    (PRIORITY_OPTION_MEDIUM, 'Medium'),
    (PRIORITY_OPTION_HIGH, 'High'),
)


class List(models.Model):

    name = models.CharField(max_length=60)
    priority = models.CharField(max_length=20,choices=PRIORITY_OPTIONS,default='low',)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', User), related_name='todo_created_by', default='')
    assigned_to = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', User), blank=True, null=True, related_name='todo_assigned_to', default='')
    due_date = models.DateField(blank=True, null=True, )
    def __str__(self):
        return self.name

    def incomplete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Task.objects.filter(list=self, completed=0)

    def complete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Task.objects.filter(list=self, completed=1)

    def num_of_incomplete_tasks(self):
        return len(self.incomplete_tasks())

    def get_priority_name(self):
        if int(self.priority) == PRIORITY_OPTION_HIGH:
            return 'High'
        if int(self.priority) == PRIORITY_OPTION_MEDIUM:
            return 'Medium'
        return 'Low'

    def num_of_complete_tasks(self):
        return len(self.complete_tasks())

    class Meta:
        ordering = ["priority","due_date"]
        verbose_name_plural = "Lists"


class Task(models.Model):
    title = models.CharField(max_length=140)
    list = models.ForeignKey(List)
    created_date = models.DateField(auto_now=True)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', User), related_name='todo_task_created_by')
    assigned_to = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', User), blank=True, null=True, related_name='todo_task_assigned_to')
    note = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_OPTIONS,default=PRIORITY_OPTION_LOW,)

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

    def is_complete(self):
        return self.completed

    def get_priority_name(self):
        if int(self.priority) == PRIORITY_OPTION_HIGH:
            return 'High'
        if int(self.priority) == PRIORITY_OPTION_MEDIUM:
            return 'Medium'
        return 'Low'

    def get_comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.title

    # Auto-set the item creation / completed date
    def save(self):
        # If Item is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    class Meta:
        ordering = ["priority"]


class Comment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    author = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', User))
    task = models.ForeignKey(Task)
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=True, null=True)

    def snippet(self):
        # Define here rather than in __str__ so we can use it in the admin list_display
        return "{author} - {snippet}...".format(author=self.author, snippet=self.body[:35])

    def __str__(self):
        return self.snippet

    class Meta:
        ordering = ["-date"]