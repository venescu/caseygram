from django.contrib import admin
from .models import Post, PostImage, Comment, Like


class PostImageInLine(admin.TabularInline):
    model = PostImage
    extra = 3


# class CommentInLine(admin.StackedInline):
#     model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInLine]


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)
