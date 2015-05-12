from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from blogApp.models import Post
from blogApp.forms import BlogPostForm, UploadImageForm

# import logging
# logger = logging.getLogger(__name__)

def view_post(request, slug):
	context = {
        'post': get_object_or_404(Post, slug=slug),
    }

	return render(request, 'blogApp/post.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_post(request):
	if request.method == "GET":
		return render(request, 'blogApp/create.html', {
			'blog_post_form': BlogPostForm(),
			'image_form': UploadImageForm(),
		})

	else:
		form = BlogPostForm(request.POST)

		if form.is_valid():
			new_post = form.save()

			messages.success(request, 'Blog post was added.')
			return redirect(new_post)

		else: # not valid, return errors
			return render(request, 'blogApp/create.html', {
				'blog_post_form': form,
				'image_form': UploadImageForm()
			})


@user_passes_test(lambda u: u.is_superuser)
def edit_post(request, slug):
	instance = get_object_or_404(Post.objects.filter(slug=slug))

	if request.method == "GET": return render( request, 'blogApp/create.html', {
		'blog_post_form': BlogPostForm(instance=instance),
		'image_form': UploadImageForm()
	})

	else:
		form = BlogPostForm(request.POST or None, instance=instance)

		if form.is_valid():
			new_post = form.save()

			messages.success(request, 'Blog post was added.')
			return redirect(new_post)

		else: # not valid, return errors
			return render(request, 'blogApp/create.html', {
				'blog_post_form': form,
				'image_form': UploadImageForm()
			})
