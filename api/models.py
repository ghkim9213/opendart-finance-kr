from django.db import models

# Create your models here.

class Content(models.Model):
    METHOD_CHOICES = [
        ('post', 'create'),
        ('get', 'read'),
        ('put', 'update'),
        ('delete', 'delete')
    ]
    method = models.CharField(max_length=8, choices=METHOD_CHOICES)
    summary = models.CharField(max_length=128)
    description = models.TextField()
    path = models.CharField(max_length=128)

    def __str__(self):
        return self.path


class ContentTag(models.Model):
    content = models.ManyToManyField(
        Content,
        related_name = 'tags',
    )
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class ContentParameter(models.Model):
    IS_IN_CHOICES = [
        ('query', 'query string'),
        ('path', 'path'),
    ]
    TYPE_CHOICES = [
        ('array', 'array'),
        ('string', 'string'),
        ('integer', 'integer'),
    ]
    content = models.ForeignKey(
        Content,
        related_name = 'parameters',
        on_delete = models.CASCADE,
    )
    name = models.CharField(max_length=128)
    is_in = models.CharField(max_length=16, choices=IS_IN_CHOICES)
    description = models.TextField()
    required = models.BooleanField()
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    format = models.CharField(max_length=16, null=True)

    def __str__(self):
        return f"{self.name} ({self.content.__str__()}): {self.description}"


class ContentResponse(models.Model):
    content = models.ForeignKey(
        Content,
        related_name = 'responses',
        on_delete = models.CASCADE,
    )
    code = models.CharField(max_length=3)
    description = models.TextField()

    def __str__(self):
        desc = '_'.join([x.upper() for x in self.description.split(' ')])
        return f"HTTP_{self.code} ({self.content.__str__()}): {self.description}"
