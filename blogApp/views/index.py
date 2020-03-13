from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blogApp.models import Post

from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# import logging
# logger = logging.getLogger(__name__)
@xframe_options_exempt
def index(request):
	POSTS_PER_PAGE = 5
	
	if request.user.is_superuser:
		post_list = Post.objects.all().order_by('-post_date')
	else:
		#post_list = Post.objects.filter(published=True).order_by('-post_date')
		post_list = get_Posts_By_Language_Code(request.LANGUAGE_CODE)

	paginator = Paginator(post_list, POSTS_PER_PAGE)

	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range, deliver last page of results.
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blogApp/index.html', {'posts': posts})

def get_Posts_By_Language_Code(language_code):
        if language_code == 'fr':
                return Post.objects.filter(language='fr', published=True).order_by('-post_date')
        else:
                return Post.objects.filter(published=True).exclude(language='fr').order_by('-post_date')
        
