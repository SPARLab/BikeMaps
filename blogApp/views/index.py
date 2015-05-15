from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blogApp.models import Post

# import logging
# logger = logging.getLogger(__name__)

def index(request):
	POSTS_PER_PAGE = 5

	if request.user.is_superuser:
		post_list = Post.objects.all().order_by('-date')
	else:
		post_list = Post.objects.filter(published=True).order_by('-date')

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
