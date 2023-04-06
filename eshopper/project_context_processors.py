from product.models import Category
from home.models import Setting

def global_category_context(request):
    return dict(
        global_categories=Category.objects.all()
    )
def global_setting_context(request):
    return dict(
        global_settings=Setting.objects.all()
    )