from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save
from .models import Article, Tag, Category, Comment
from .forms import ArticleForm, CategoryForm, TagForm, CommentForm

#==========================Système de gestion des rôles=============================
# Création des groupes 
def create_groups():
    admin_group, _ = Group.objects.get_or_create(name='Administrateurs')
    editeur_group, _ = Group.objects.get_or_create(name='Éditeurs')
    visiteur_group, _ = Group.objects.get_or_create(name='Visiteurs')

    # Permissions pour les Administrateurs (toutes les permissions)
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # Permissions pour les Éditeurs (CRUD sur Article et Tag)
    editeur_permissions = Permission.objects.filter(codename__in=[
        'add_article', 'change_article', 'delete_article', 'view_article',
        'add_tag', 'change_tag', 'delete_tag', 'view_tag'
    ])
    editeur_group.permissions.set(editeur_permissions)

    # Les visiteurs n'ont que la permission de voir des articles
    visiteur_permissions = Permission.objects.filter(codename='view_article')
    visiteur_group.permissions.set(visiteur_permissions)



# Ajouter automatiquement l'utilisateur au groupe des Éditeurs lors de l'inscription
def add_user_to_editeur_group(sender, instance, created, **kwargs):
    if created:
        editeur_group = Group.objects.get(name='Éditeurs')
        instance.groups.add(editeur_group)

#==============================Article===============================
# Afficher la liste des articles (Éditeurs et Administrateurs)
class ArticleListeViews(generic.ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'Articles/article_list.html'

    def get_queryset(self):
        return Article.objects.all().order_by('-updated_at')

# Créer un nouvel article (Éditeurs et Administrateurs)
class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'Articles/article_form.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirection vers la page de connexion
        return super().dispatch(request, *args, **kwargs)

# Modifier un article existant (Éditeurs et Administrateurs)
class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'Articles/article_form.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        # Permettre uniquement aux auteurs de modifier leurs propres articles
        return Article.objects.filter(author=self.request.user)

# Supprimer un article (Éditeurs et Administrateurs)
class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Article
    template_name = 'Articles/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        # Permettre uniquement aux auteurs de supprimer leurs propres articles
        return Article.objects.filter(author=self.request.user)

# Afficher les détails d'un article (Accessible à tous les utilisateurs connectés)
class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'Articles/article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
       
        user = self.request.user

        # Ajoutez les droits d'édition et de suppression pour les auteurs et les administrateurs
        if user.is_authenticated:
            context['can_edit'] = user == article.author or user.is_superuser
            context['can_delete'] = user == article.author or user.is_superuser
            context['can_comment'] = True
            context['user_comments'] = article.commentaire.filter(author=user)
            context['form'] = CommentForm()
        else:
            context['can_edit'] = False
            context['can_delete'] = False
            context['can_comment'] = False
            context['user_comments'] = []
            
            

        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = self.get_object()
            commentaire.author = request.user
            commentaire.save()
        return redirect('article_detail', pk=self.get_object().pk)

#==============================Categorie et Tag===============================

# Vues pour Category (Admin et Éditeurs uniquement)
class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'categorie/category_list.html'

class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categorie/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categorie/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    template_name = 'categorie/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

# Vues pour Tag (Admin et Éditeurs uniquement)
class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'tag/tag_list.html'

class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tag/tag_form.html'
    success_url = reverse_lazy('tag_list')

class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tag/tag_form.html'
    success_url = reverse_lazy('tag_list')

class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    template_name = 'tag/tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')

#==============================Commentaires===============================

# Ajouter un commentaire à un article (Accessible à tous les utilisateurs connectés)
class CommentCreateView(View):
    @method_decorator(login_required)
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user  # Associe l'auteur connecté
            comment.save()
        return redirect('article_detail', pk=article_id)

# Modifier un commentaire existant (Accessible à l'auteur du commentaire ou aux administrateurs)
class CommentUpdateView(View):
    @method_decorator(login_required)
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(instance=comment)
        return render(request, 'commentaire/comment_update.html', {'form': form})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=comment.article.id)

# Supprimer un commentaire existant (Accessible à l'auteur du commentaire ou aux administrateurs)
class CommentDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return render(request, 'commentaire/comment_delete.html', {'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        article_id = comment.article.id
        comment.delete()
        return redirect('article_detail', pk=article_id)
