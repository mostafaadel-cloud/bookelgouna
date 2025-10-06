from ckeditor.fields import RichTextField
from easy_thumbnails.fields import ThumbnailerImageField
from hvad.manager import TranslationManager
from hvad.models import TranslatableModel, TranslatedFields

from django.db import models
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail

from common.models import AbstractComment
from users.models import User


class Category(TranslatableModel):
    icon = ThumbnailerImageField(verbose_name=_('Icon'), blank=True, upload_to='uploads',
                                 help_text=_('add 18x18 image or bigger (then it will be cropped) '
                                             'otherwise default icon will be used'))
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, unique=True)

    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("Name"), max_length=255, unique=True),
    )

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def category_icon_thumbnail(self):
        return self.icon['blog_category_icon'].url

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('order',)

    def __unicode__(self):
        return self.name_trans

    @models.permalink
    def get_absolute_url(self):
        return 'blog_category', (), {'slug': self.slug}

    @property
    def name_trans(self):
        return self.lazy_translation_getter('name')


class OrderedBlogPostsManager(TranslationManager):
    def get_queryset(self):
        return super(OrderedBlogPostsManager, self).get_queryset().order_by('-created')


class BlogPost(TranslatableModel):
    category = models.ForeignKey(Category, verbose_name=_("Category"), related_name="posts")
    featured_image = ThumbnailerImageField(verbose_name=_("Featured Image"), upload_to='uploads')
    crop = ImageRatioField('featured_image', verbose_name='Crop', size='1000x400')
    video_link = models.CharField(verbose_name=_('Video'), blank=True, max_length=255,
                                  help_text=_('youtube video link like http://www.youtube.com/watch?v=_oPAwA_Udwc. '
                                              'do not use embeded youtube link here.'))
    video_id = models.CharField(blank=True, max_length=20)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255, unique=True),
        desc_metatag=models.CharField(_('description metatag'), max_length=160, help_text=_('max length is 160 letters')),
        text=RichTextField(verbose_name=_("Long Description"))
    )

    objects = OrderedBlogPostsManager()

    def featured_image_thumbnail(self):
        if self.featured_image:
            if self.crop:
                return cropped_thumbnail({}, self, 'crop')
            else:
                return self.featured_image['blog_post_image'].url

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        return self.title_trans

    @models.permalink
    def get_absolute_url(self):
        return 'post', (), {'slug': self.slug}

    @property
    def title_trans(self):
        return self.lazy_translation_getter('title')

    @property
    def desc_metatag_trans(self):
        return self.lazy_translation_getter('desc_metatag')

    @property
    def text_trans(self):
        return self.lazy_translation_getter('text')


class PostImage(models.Model):
    post = models.ForeignKey(BlogPost, verbose_name=_("Post"), related_name="images")
    image = ThumbnailerImageField(verbose_name=_('Image'), upload_to='uploads')
    crop = ImageRatioField('image', verbose_name='Crop', size='1000x400')

    def post_icon_thumbnail(self):
        if self.image:
            if self.crop:
                return cropped_thumbnail({}, self, 'crop')
            else:
                return self.image['blog_post_image'].url


class BlogComment(AbstractComment):
    entity = models.ForeignKey(BlogPost, verbose_name=_('Post'), related_name='comments')
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='post_comments')

    def __unicode__(self):
        return u"{}'s comment".format(self.creator.email)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('-created',)


class ApprovedBlogCommentManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedBlogCommentManager, self).get_queryset().filter(is_approved=True)


# Use these models for admin only. Use BlogComment model to fetch comments for site.
class ApprovedBlogComment(BlogComment):

    objects = ApprovedBlogCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (approved)')
        verbose_name_plural = _('Comments (approved)')


class UnapprovedBlogCommentManager(models.Manager):
    def get_queryset(self):
        return super(UnapprovedBlogCommentManager, self).get_queryset().filter(is_approved=False)


class UnapprovedBlogComment(BlogComment):

    objects = UnapprovedBlogCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (unapproved)')
        verbose_name_plural = _('Comments (unapproved)')
