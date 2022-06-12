from .models import Country

def menu_links(request):
    links=Country.objects.all()
    return dict(links=links)

