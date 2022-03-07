from django.db import models
import uuid

from django.db.models.deletion import SET_NULL

from users.models import Profile

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=SET_NULL)
    title = models.CharField(max_length=2000, blank=True)
    description = models.TextField(blank=True)
    vote_ratio = models.IntegerField(null=True, blank=True)
    vote_total = models.IntegerField(null=True, blank=True)
    featured_image = models.ImageField(blank=True, null=True, default='default.jpg')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

    @property
    def query_review(self):
        reviews = self.review_set.all().values_list('owner__id', flat=True)
        return reviews


    @property
    def update_info(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_ratio = ratio
        self.vote_total = totalVotes
        self.save()

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

class Review(models.Model):
    Vote_Type = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=5 ,choices=Vote_Type)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
