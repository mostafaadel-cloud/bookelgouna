from urlparse import urlparse, parse_qs
from adminsortable.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from hvad.admin import TranslatableAdmin
from hvad.forms import TranslatableModelForm
from image_cropping import ImageCroppingMixin

from django.utils.translation import ugettext_lazy as _

from .models import BlogPost, Category, PostImage, ApprovedBlogComment, UnapprovedBlogComment


class CategoryForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = Category.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The blog category with this Name already exists.")
        return name


class CategoryAdmin(SortableAdminMixin, TranslatableAdmin):
    list_display = ('__unicode__', 'slug')
    form = CategoryForm

    # Workaround for prepopulated_fields and fieldsets from here:
    # https://github.com/KristianOellegaard/django-hvad/issues/10#issuecomment-5572524
    def __init__(self, *args, **kwargs):
        super(CategoryAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {"slug": ("name",)}
        self.fieldsets = (
            ('Translatable', {
                'fields': ('name',)
            }),
            ('Non-translatable', {
                'fields': ('slug', 'icon',)
            }),
        )


class ApprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved', 'language')


class UnapprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved', 'language')


class ImageInlineModelForm(forms.ModelForm):
    def save(self, commit=True):
        # clear crop field if post image inline already exists and image is changed
        if self.instance.pk is not None and 'image' in self.changed_data:
            self.instance.crop = None
        return super(ImageInlineModelForm, self).save(commit)

    class Meta:
        model = PostImage
        fields = ('post', 'image', 'crop')


class ImageInlineModelAdmin(ImageCroppingMixin, admin.TabularInline):
    form = ImageInlineModelForm
    model = PostImage


def parse_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None


class BlogPostTranslatableModel(TranslatableModelForm):
    def save(self, commit=True):
        video_link = self.cleaned_data.get('video_link')
        if video_link:
            self.instance.video_id = parse_video_id(video_link)
        # clear crop field if blog post already exists and image is changed
        if self.instance.pk is not None and 'featured_image' in self.changed_data:
            self.instance.crop = None
        return super(BlogPostTranslatableModel, self).save(commit)

    def clean_video_link(self):
        video_link = self.cleaned_data.get('video_link')
        if video_link:
            video_id = parse_video_id(video_link)
            if not video_id:
                raise forms.ValidationError(_('Youtube link is incorrect.'))
        return video_link

    def clean_title(self):
        title = self.cleaned_data['title']
        q = BlogPost.objects.language('all').filter(title=title)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The blog post with this Title already exists.")
        return title


class BlogPostAdmin(ImageCroppingMixin, TranslatableAdmin):
    list_display = ('__unicode__', 'slug', 'category', 'created')
    inlines = [ImageInlineModelAdmin]
    form = BlogPostTranslatableModel

    # Workaround for prepopulated_fields and fieldsets from here:
    # https://github.com/KristianOellegaard/django-hvad/issues/10#issuecomment-5572524
    def __init__(self, *args, **kwargs):
        super(BlogPostAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {"slug": ("title",)}

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'desc_metatag', 'text')
            }),
            ('Non-translatable', {
                'fields': ('slug', 'category', 'video_link')
            }),
            ('Featured image', {
                'fields': ('featured_image',)
            })
        ]

        if obj is not None:
            del fieldsets[-1]
            fieldsets.append(
                ('Featured image and its cropping', {
                    'fields': (('featured_image', 'crop'),)
                })
            )
        self.fieldsets = fieldsets
        return super(BlogPostAdmin, self).get_fieldsets(request, obj)


admin.site.register(ApprovedBlogComment, ApprovedCommentAdmin)
admin.site.register(UnapprovedBlogComment, UnapprovedCommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
