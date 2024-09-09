from django import forms
from .models import Article,Category, Tag,Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'categories', 'tags']
        labels = {
            'title': 'Titre',
            'content': 'Contenu',
            'image': 'Photo',
            'categories': 'Catégorie',
            'tags': 'Étiquette'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le titre de l\'article'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Entrez le contenu de l\'article'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'height: auto;'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'height: auto;'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Nom'}

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {'name': 'Nom'}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Commentaire'
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

