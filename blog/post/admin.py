from django.contrib import admin

from .models import Post
from .models import Post 
from .models import Images 
from .models import Comment 
from .models import Tag 
from .models import Category 
from .models import Like 

# Register your models here.

admin.site.register(Post)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Like)