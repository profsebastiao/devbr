from django.db import models
from django import forms
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


# --- SNIPPET DE CATEGORIA ---
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField("Nome da Categoria", max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='Um identificador para URL (ex: noticias-do-brasil)',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


# --- SNIPPET DE AUTOR ---
@register_snippet
class BlogAuthor(models.Model):
    name = models.CharField("Nome do Autor", max_length=100)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('image'),
    ]

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.name


# --- SUA HOME PAGE ---
class HomePage(Page):
    texto_boas_vindas = models.CharField(max_length=255, blank=True)
    
    body = StreamField([
        ('titulo', blocks.CharBlock(form_classname="title")),
        ('paragrafo', blocks.RichTextBlock()),
        ('citacao', blocks.BlockQuoteBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('texto_boas_vindas'),
        FieldPanel('body'),
    ]


# --- SUA PÁGINA PADRÃO (SOBRE MIM, ETC) ---
class StandardPage(Page):
    intro = models.CharField("Introdução", max_length=250, blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    body = StreamField([
        ('titulo', blocks.CharBlock(form_classname="title")),
        ('paragrafo', blocks.RichTextBlock()),
        ('codigo', blocks.StructBlock([
            ('linguagem', blocks.ChoiceBlock(choices=[
                ('python', 'Python'), ('html', 'HTML'), ('bash', 'Terminal'),
            ], label="Linguagem")),
            ('code_text', blocks.TextBlock(label="Cole seu código aqui")),
        ], icon='code')), 
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('main_image'),
        FieldPanel('body'),
    ]


# --- TAGS DO BLOG ---
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage', 
        related_name='tagged_items', 
        on_delete=models.CASCADE
    )


# --- SUA PÁGINA DE BLOG ---
class BlogPage(Page):
    date = models.DateField("Data do Post")
    intro = models.CharField("Introdução", max_length=250)
    
    # Campos de Relação
    categories = ParentalManyToManyField('home.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    
    author = models.ForeignKey(
        'home.BlogAuthor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    body = StreamField([
        ('titulo', blocks.CharBlock(form_classname="title")),
        ('paragrafo', blocks.RichTextBlock()),
        ('codigo', blocks.StructBlock([
            ('linguagem', blocks.ChoiceBlock(choices=[
                ('python', 'Python'), ('html', 'HTML'), ('bash', 'Terminal'),
            ], label="Linguagem")),
            ('code_text', blocks.TextBlock(label="Cole seu código aqui")),
        ], icon='code')), 
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        
        # --- CORREÇÃO: Adicionei o painel do Autor aqui ---
        FieldPanel('author'),
        # --------------------------------------------------
        
        FieldPanel('intro'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('main_image'),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]


# --- MODELO DOS CAMPOS DO FORMULÁRIO ---
class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


# --- A PÁGINA DE CONTATO ---
class FormPage(AbstractEmailForm):
    intro = RichTextField("Texto Introdutório", blank=True)
    thank_you_text = RichTextField("Texto de Agradecimento", blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Campos do Formulário"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Configurações de E-mail"),
    ]