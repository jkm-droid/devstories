from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag

from portal.forms import WriteStoryForm, EditProfileForm, UserProfileForm, CommentForm, ChangePassword
from .models import Story, Comments, Like, Smile, StoryViews, SaveForLater, UserProfile


# function to get the number of added posts
def get_notifications():
    notice = Story.objects.filter(is_seen=False).count()
    if notice < 1:
        notice = 0
        return notice
    else:
        return notice


"""
the function displays the index/portal page and
lists all the stories in the database and common tags
"""


def index_view(request):
    if request.user.is_authenticated:
        template_name = 'portal/portal.html'

        posts = Story.objects.filter(draft=False).order_by('-created_on')
        latest_stories = Story.objects.filter(draft=False).order_by('-created_on')[:3]
        tags = Story.tags.most_common()[:4]
        common_tags = Story.tags.all()
        is_search = True
        darkmode = True
        notice = get_notifications()

        context = {
            'all_posts': posts,
            'tags': tags,
            'common_tags': common_tags,
            'latest_stories': latest_stories,
            'is_search': is_search,
            'darkmode': darkmode,
            'notice': notice
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
this function displays the form for writing a new story
"""


def write_story_view(request):
    if request.user.is_authenticated:
        darkmode = True
        form = WriteStoryForm()

        template_name = 'portal/writestory.html'
        title = f"{request.user.username}, you are now writing a new story..."

        if request.method == "POST":
            author = Story(author=request.user)
            form = WriteStoryForm(request.POST, request.FILES, instance=author)
            if form.is_valid():
                story = form.save(commit=False)
                story.save()
                form.save_m2m()
                messages.info(request, "Post published successfully")
                return redirect('dashboard')

        else:
            form = WriteStoryForm()
        notice = get_notifications()
        context = {
            "form": form,
            'title': title,
            'darkmode': darkmode,
            'notice': notice
        }
        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in to post a story")
        return redirect('login')


"""
this function enables the user to edit the a story based on its id
"""


def edit_story_view(request, id):
    if request.user.is_authenticated:
        darkmode = True
        is_edit = True
        story = get_object_or_404(Story, id=id)
        form = WriteStoryForm(request.POST or None, request.FILES or None, instance=story)
        title = f"{request.user.username}, you are now editing your story..."
        if form.is_valid():
            form.save()
            messages.info(request, "Post updated successfully")
            return redirect('dashboard')

        notice = get_notifications()
        context = {
            'form': form,
            'title': title,
            'darkmode': darkmode,
            "is_edit": is_edit,
            'notice': notice
        }
        template_name = 'portal/writestory.html'

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
this function displays the drafted posts on the user dashboard
"""


def drafted_stories_view(request):
    if request.user.is_authenticated:
        template_name = 'portal/draftedstories.html'
        darkmode = True
        # get all the posts belonging to the logged user
        posts = Story.objects.filter(author=request.user, draft=True).order_by('-created_on')
        number_of_posts = Story.objects.filter(author=request.user, draft=False).count()
        number_of_drafts = Story.objects.filter(author=request.user, draft=True).count()

        tags = Story.tags.all()
        notice = get_notifications()
        context = {
            'posts': posts,
            'number_of_posts': number_of_posts,
            'number_of_drafts': number_of_drafts,
            'tags': tags,
            'darkmode': darkmode,
            'notice': notice
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
function to display a user's reading list
"""


def reading_list_view(request):
    if request.user.is_authenticated:
        template_name = "portal/readinglist.html"
        darkmode = True
        posts = Story.objects.filter(is_saved=True).order_by('-created_on')

        tags = Story.tags.all()
        notice = get_notifications()
        context = {
            'posts': posts,
            'tags': tags,
            'darkmode': darkmode,
            'notice': notice
        }

        return render(request, template_name, context)


"""
this function displays the user's stories (both published and drafted)
"""


def dashboard_view(request):
    if request.user.is_authenticated:
        template_name = 'portal/dashboard.html'
        darkmode = True
        # get all the posts belonging to the logged user
        posts = Story.objects.filter(author=request.user, draft=False).order_by('-created_on')
        number_of_posts = Story.objects.filter(author=request.user, draft=False).count()
        number_of_drafts = Story.objects.filter(author=request.user, draft=True).count()

        tags = Story.tags.all()
        notice = get_notifications()
        context = {
            'posts': posts,
            'number_of_posts': number_of_posts,
            'number_of_drafts': number_of_drafts,
            'tags': tags,
            'darkmode': darkmode,
            'notice': notice
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
a function to display the edit profile form for changing personal
details
"""


def settings_profile_view(request):
    if request.user.is_authenticated:
        template_name = 'portal/settings.html'
        darkmode = True

        if request.method == "POST":
            edit_form = EditProfileForm(request.POST, instance=request.user)
            user_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if edit_form.is_valid() and user_form.is_valid():
                profile = user_form.save(commit=False)
                profile.is_profile = True
                profile.save()
                edit_form.save()

                messages.info(request, "Your profile updated successfully")
                return redirect('dashboard')
        else:
            edit_form = EditProfileForm(instance=request.user)
            user_form = UserProfileForm(instance=request.user.profile)

        pass_form = ChangePassword(request.user)

        if request.is_ajax() and request.method == "POST":
            pass_form = ChangePassword(request.user, request.POST)
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            username = request.user.username
            user = authenticate(username=username, password=old_password)

            if user is not None:
                # check if passwords are not empty
                if new_password2 != '' and new_password2 != '':
                    # check if the two passwords match
                    if new_password1 == new_password2:
                        new_user = User.objects.get(username=username)
                        new_user.set_password(new_password1)
                        new_user.save()
                        update_session_auth_hash(request, new_user)

                        response = {
                            'success': "Successfully changed password"
                        }
                        print(response)

                        return JsonResponse(response)
                    else:
                        response = {
                            'error': "Error...The two passwords did not match"
                        }
                        print(response)

                        return JsonResponse(response)
                else:
                    data = {
                        'error': "Error...Passwords cannot be empty"
                    }

                    return JsonResponse(data)
            else:
                data = {
                    'error': "An error occurred...Please try again"
                }

                return JsonResponse(data)
        else:
            pass_form = ChangePassword(request.user)
        notice = get_notifications()
        context = {
            'edit_form': edit_form,
            'user_form': user_form,
            'darkmode': darkmode,
            'pass_form': pass_form,
            'notice': notice
        }

        return render(request, template_name, context)

    else:
        messages.info(request, "You must be logged in to edit profile")
        return redirect('login')


"""
the function displays stories based on a specific tag name
"""


def tagged_stories_view(request, slug):
    if request.user.is_authenticated:
        darkmode = True
        template_name = "portal/taggedstories.html"
        tags = get_object_or_404(Tag, slug=slug)
        stories = Story.objects.filter(tags=tags, draft=False)
        notice = get_notifications()

        context = {
            'stories': stories,
            'tags': tags,
            'darkmode': darkmode,
            'notice': notice
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
a function to display a single story and the user profile
"""


def full_story_view(request, slug):
    if request.user.is_authenticated:
        template_name = "portal/fullstory.html"
        darkmode = True

        try:
            story = Story.objects.get(slug=slug)
            story.is_seen = True
            story.save()
        except:
            raise Http404
        author_id = story.author.id
        tags = Story.tags.all()
        author_user = User.objects.get(pk=author_id)

        # get the number of stories the user has written
        no_of_stories = Story.objects.filter(author=author_user).count()

        if no_of_stories <= 1:
            author_user.profile.status = "BEGINNER"
            author_user.save()

        elif 1 < no_of_stories <= 10:
            author_user.profile.status = "INTERMEDIATE"
            author_user.save()
        else:
            author_user.profile.status = "PRO"
            author_user.save()

        # get more stories written by the author
        more_stories = Story.objects.filter(author=author_user)
        title = ''
        for more in more_stories:
            if more.slug != slug:
                title = f"More stories from {author_user}"

        form = CommentForm()
        if request.is_ajax():
            body = request.POST.get('body')
            username = request.user

            comments = Comments(
                username=username,
                body=body,
                story=story
            )

            comments.save()
            CommentForm()
            response = {
                'message': 'Comment Saved successfully'
            }

            return JsonResponse(response)

        comment_list = Comments.objects.filter(story=story).order_by('-created_on')
        comments_no = Comments.objects.filter(story=story).count()
        notice = get_notifications()
        context = {
            "story": story,
            "author": author_user,
            'tags': tags,
            'form': form,
            'comments': comment_list,
            'comments_no': comments_no,
            'more_stories': more_stories,
            'darkmode': darkmode,
            'title': title,
            'notice': notice
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
this function deletes a post based on its unique slug
"""


def delete_story_view(request, slug):
    if request.user.is_authenticated:
        story = get_object_or_404(Story, slug=slug)
        if request.method == "POST":
            story.delete()
            messages.info(request, "Story deleted successfully")
            return redirect('dashboard')

        template_name = 'portal/deletestory.html'
        context = {
            'story': story
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
a function to add the number of likes per story
a second click de-registers the like
"""


def like_view(request, story_id, userpreference):
    if request.user.is_authenticated:
        template_name = 'portal/fullstory.html'
        if request.method == "POST":
            story = get_object_or_404(Story, id=story_id)
            try:
                like_object = Like.objects.get(user=request.user, story=story)
                value_object = like_object.value
                value_object = int(value_object)
                user_like = int(userpreference)

                if value_object != user_like:
                    like_object.delete()

                    like = Like()
                    like.user = request.user
                    like.story = story
                    like.value = user_like

                    if user_like == 1 and value_object != 1:
                        story.likes += 1

                    like.save()
                    story.save()
                    response = {
                        'message': 'Liked'
                    }

                    return JsonResponse(response)

                elif value_object == user_like:
                    like_object.delete()
                    if user_like == 1:
                        story.likes -= 1

                    story.save()
                    response = {
                        'message': 'Unliked'
                    }

                    return JsonResponse(response)

            except Like.DoesNotExist:
                like = Like()
                like.user = request.user
                like.story = story
                like.value = userpreference
                user_like = int(userpreference)

                if user_like == 1:
                    story.likes += 1
                like.save()
                story.save()

                response = {
                    'message': 'Liked'
                }

                return JsonResponse(response)

        return render(request, template_name, {})
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
a function to add the number of smiles per story
it adds and deducts smiles depending on user clicks
"""


def smile_view(request, story_id, userpreference):
    if request.user.is_authenticated:
        template_name = 'portal/fullstory.html'
        if request.method == "POST":
            story = get_object_or_404(Story, id=story_id)
            try:
                smile_object = Smile.objects.get(user=request.user, story=story)
                value_object = smile_object.value
                value_object = int(value_object)
                user_smile = int(userpreference)

                if value_object != user_smile:
                    smile_object.delete()

                    smile = Smile()
                    smile.user = request.user
                    smile.story = story
                    smile.value = user_smile

                    if user_smile == 2 and value_object != 2:
                        story.smiles += 1

                    smile.save()
                    story.save()
                    response = {
                        'message': 'Smiled'
                    }

                    return JsonResponse(response)

                elif value_object == user_smile:
                    smile_object.delete()
                    if user_smile == 2:
                        story.smiles -= 1

                    story.save()
                    response = {
                        'message': 'Desmile'
                    }

                    return JsonResponse(response)

            except Smile.DoesNotExist:
                smile = Smile()
                smile.user = request.user
                smile.story = story
                smile.value = userpreference
                user_smile = int(userpreference)

                if user_smile == 2:
                    story.smiles += 1
                smile.save()
                story.save()
                response = {
                    'message': 'Smiled'
                }

                return JsonResponse(response)

        return render(request, template_name, {})
    else:
        messages.info(request, "You must be logged in")
        return redirect("login")


"""
the function to register the number of views per every story
each user receives a single view
"""


def register_user_views(request, story_id, userview):
    template_name = "portal/fullstory.html"
    if request.is_ajax():
        story = get_object_or_404(Story, id=story_id)
        try:
            userview_object = StoryViews.objects.get(user=request.user, story=story)
            value_object = userview_object.value
            value_object = int(value_object)
            userview = int(userview)

            if value_object != userview:
                userview_object.delete()

                view = StoryViews()
                view.user = request.user
                view.story = story
                view.value = userview

                if userview == 3 and value_object != 3:
                    story.views += 1

                view.save()
                story.save()
                msg = "Story viewed"

                response = {
                    'msg': msg
                }

                return JsonResponse(response)

        except StoryViews.DoesNotExist:
            view = StoryViews()
            view.user = request.user
            view.story = story
            view.value = userview
            userview = int(userview)

            if userview == 3:
                story.views += 1
            view.save()
            story.save()

            response = {
                'msg': 'Story Viewed in exception'
            }

            return JsonResponse(response)

    return render(request, template_name)


"""
    function to check the status of story, whether it is added into reading list or not
"""


def check_saved_status(request, story_id):
    if request.user.is_authenticated:
        template_name = "portal/portal.html"
        if request.is_ajax():
            story = get_object_or_404(Story, id=story_id)

            if story.is_saved:

                response = {
                    'status': 'saved'
                }
                return JsonResponse(response)
            else:

                response = {
                    'status': 'unsaved'
                }
                return JsonResponse(response)

        return render(request, template_name, {})


''''
    function to save a user's stories for later reading
'''


def save_story_for_later_view(request, story_id, usersave):
    if request.user.is_authenticated:
        template_name = "portal/portal.html"

        if request.is_ajax() and request.method == "POST":
            story = get_object_or_404(Story, id=story_id)
            try:
                usersave_object = SaveForLater.objects.get(user=request.user, story=story)
                value_object = usersave_object.value
                value_object = int(value_object)
                usersave = int(usersave)

                if value_object != usersave:
                    usersave_object.delete()

                    saveforlater = SaveForLater()
                    saveforlater.user = request.user
                    saveforlater.story = story
                    saveforlater.value = usersave

                    if usersave == 7241996 and value_object != 7241996:
                        story.is_saved = True
                    saveforlater.save()
                    story.save()
                    story_id = int(story_id)
                    # save
                    response = {
                        'message': "saved",
                        'postid': story_id
                    }

                    return JsonResponse(response)

                elif value_object == usersave:
                    usersave_object.delete()
                    if usersave == 7241996:
                        story.is_saved = False
                    story.save()
                    story_id = int(story_id)
                    # unsave
                    response = {
                        "message": "unsaved",
                        "postid": story_id
                    }

                    return JsonResponse(response)

            except SaveForLater.DoesNotExist:
                saveforlater = SaveForLater()
                saveforlater.user = request.user
                saveforlater.story = story
                saveforlater.value = usersave
                usersave = int(usersave)

                if usersave == 7241996:
                    story.is_saved = True
                saveforlater.save()
                story.save()
                story_id = int(story_id)
                # save
                response = {
                    'message': "saved",
                    'postid': story_id
                }

                return JsonResponse(response)

        return render(request, template_name, {})
    else:
        messages.info(request, "You must be logged in")
        return redirect("login")


'''
     function for performing search
'''


def search_view(request):
    if request.method == "GET":
        query = request.GET.get('q')
        if query:
            results = Story.objects.filter(
                Q(title__icontains=query) |
                Q(title__iexact=query)).distinct().order_by('-created_on')

            template_name = "portal/search.html"
            is_search = True

            context = {
                'results': results,
                'query': query,
                'is_search': is_search
            }

            return render(request, template_name, context)

        else:
            messages.info(request, "You cannot search for an empty string")
            return redirect('portal')


"""
function to de-activate a users account
"""


def deactivate_users_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.user
            user = User.objects.get(username=username)
            user.is_active = False
            user.delete()
            messages.info(request, "Account deleted successfully")
            return redirect('login')

        else:
            messages.info(request, "An error occurred")

    else:
        messages.info(request, "You must be logged in")
        return redirect('login')


"""
    function to get all the unread stories/notifications
"""


def get_notification_view(request):
    if request.user.is_authenticated:
        template_name = 'portal/notifications.html'

        posts = Story.objects.filter(draft=False, is_seen=False).order_by('-created_on')
        is_search = True
        darkmode = True
        notice = get_notifications()

        context = {
            'all_posts': posts,
            'is_search': is_search,
            'darkmode': darkmode,
            'notice': notice
        }

        return render(request, template_name, context)
    else:
        messages.info(request, "You must be logged in")
        return redirect('login')

