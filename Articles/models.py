from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

# Table Categorie
class Category(models.Model):
    name = models.CharField(max_length=100)

    permissions = [
            ("can_add_categorie", "Can add categorie"),
            ("can_edit_categorie", "Can edit categorie"),
            ("can_delete_categorie", "Can delete categorie"),
        ]

    def __str__(self):
        return self.name

# Table Etiquette
class Tag(models.Model):
    name = models.CharField(max_length=50)

    permissions = [
            ("can_add_tag", "Can add tag"),
            ("can_edit_tag", "Can edit tag"),
            ("can_delete_tag", "Can delete tag"),
        ]
    def __str__(self):
        return self.name

# Table Article
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='articles/', blank=True)

    class Meta:
        permissions = [
            ("can_add_article", "Can add article"),
            ("can_edit_article", "Can edit article"),
            ("can_delete_article", "Can delete article"),
        ]

    def __str__(self):
        return self.title

# Table Commentaire
class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='commentaire', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_add_comment", "Can add comment"),
            ("can_edit_comment", "Can edit comment"),
            ("can_delete_comment", "Can delete comment"),
        ]

    def __str__(self):
        return f'Commentaire de {self.author} pour {self.article}'

