from django.shortcuts import render

from portal.models import Story


def home_view(request):
    template_name = 'home.html'

    posts = Story.objects.filter(draft=False).order_by('-created_on')
    latest_stories = Story.objects.filter(draft=False).order_by('-created_on')[:3]
    tags = Story.tags.most_common()[:4]
    common_tags = Story.tags.all()
    is_search = True

    context = {
        'all_posts': posts,
        'tags': tags,
        'common_tags': common_tags,
        'latest_stories': latest_stories,
        'is_search': is_search
    }

    return render(request, template_name, context)
