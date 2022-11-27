from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.user", on_delete = models.CASCADE, verbose_name = "Yazar")
    title = models.CharField(max_length = 50, verbose_name = "Başlık")
    content = models.TextField(verbose_name = "İçerik")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Oluşturma tarihi")
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Makale", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.CharField(max_length=300, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']
