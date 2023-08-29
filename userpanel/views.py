import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages import success
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Website, ContentWebsite
from .forms import WebsiteForm, ReplacePhraseForm, SelectWebsiteForm, \
    ContentWebsiteForm
from django.contrib.auth.decorators import login_required
from .scripts.main import get_wordpress_posts
from .scripts.links_process import main_script
from django.contrib import messages
from .scripts.remove import run_text_process
from .scripts.update import *
from .scripts.process_dot import *


def dashboard(request):
    return redirect('custom_login')


def profile(request):
    return render(request, 'userpanel/profile.html')


@login_required
def user_panel(request):
    user_websites = Website.objects.filter(user=request.user)
    return render(request, 'userpanel/user_panel.html',
                  {'user_websites': user_websites})


@login_required
def website_panel(requset, website_id):
    website = Website.objects.get(pk=website_id)
    contents = ContentWebsite.objects.filter(website_id=website_id)
    return render(requset, 'userpanel/website_panel.html',
                  {'website': website, 'contents': contents})


def remove_links2(request):
    if request.method == "POST":
        website_id = request.POST.get('website_id')
        all_content = ContentWebsite.objects.filter(website_id=website_id)

        aradbranding_pattern = r'<a\s+href="https?://aradbranding\.com[^>]*>(' \
                               r'.*?)</a> '
        for content in all_content:
            content.content = re.sub(aradbranding_pattern, r'\1', content.content)
            content.save()
            print(content)

        if success:
            messages.success(request, "اسکریپت با موفقیت اجرا شد")
            return redirect('add_phrase')
        # return JsonResponse({"message": "محتواها با موفقیت ویرایش شدند."})
    else:
        # درخواست GET
        return HttpResponse ('Nashod')



@login_required
def delete_website(request, website_id):
    if request.method == 'POST':
        website = Website.objects.get(pk=website_id)
        if website.user == request.user:
            website.delete()
    return redirect('user_panel')


@login_required
def add_website(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website = form.save(commit=False)
            website.user = request.user
            website.save()
            return redirect('dashboard')
    else:
        form = WebsiteForm()
    return render(request, 'userpanel/add_website.html', {'form': form})


# @login_required
# def add_phrase(request):
#     user_sites = Website.objects.filter(
#         user=request.user)  # بازیابی سایت‌های مربوط به کاربر
#     if request.method == 'POST':
#         form = ReplacePhraseForm(request.POST, user_sites=user_sites)
#         if form.is_valid():
#             phrase = form.save(commit=False)
#             phrase.user = request.user
#             phrase.save()
#             return redirect('add_phrase')
#     else:
#         form = ReplacePhraseForm(
#             user_sites=user_sites)  # ارسال لیست سایت‌ها به فرم
#
#     user_phrases = ReplacePhrase.objects.filter(user=request.user)
#     return render(request, 'userpanel/add_phrase.html', {'form': form})




@login_required
def process(request):
    return render(request, 'userpanel/process.html')


@login_required
def add_phrase(request):
    if request.method == 'POST':
        form = ReplacePhraseForm(request.POST)
        if form.is_valid():
            phrase = form.cleaned_data['phrase']
            link = form.cleaned_data['link']
            replacements = {
                phrase: link
            }

            directory = form.cleaned_data['website']
            directory = f'output/website_content/{directory}'
            directory = directory.replace('https://', '')
            main_script(directory, replacements)

            if success:
                messages.success(request, "اسکریپت با موفقیت اجرا شد")
                return redirect('add_phrase')
            else:
                messages.error(request,
                               "موفقیت‌آمیز نبود. لطفاً دوباره امتحان کنید.")
                return redirect('add_phrase')

    else:
        form = ReplacePhraseForm()

    return render(request, 'userpanel/add_phrase.html', {'form': form})


@login_required
def run_update_script_view(request):
    user = request.user

    if request.method == 'POST':
        form = SelectWebsiteForm(user, request.POST)
        if form.is_valid():
            selected_website = form.cleaned_data['website']

            # خواندن اطلاعات وبسایت از دیتابیس
            wordpress_url = selected_website.website_url
            username = selected_website.site_username
            password = selected_website.site_password
            content_folder = f'output/website_content/{selected_website.website_url}'
            content_folder = content_folder.replace('https://', '')

            # اجرای اسکریپت از فایل جداگانه
            run_wordpress_update_script(content_folder, wordpress_url, username,
                                        password)  # نام تابع تغییر کرده است
    else:
        form = SelectWebsiteForm(user)

    return render(request, 'userpanel/update-content.html', {'form': form})


@login_required
def remove_link(request):
    user = request.user
    if request.method == "POST":
        form = SelectWebsiteForm(user, request.POST)
        if form.is_valid():
            selected_website = form.cleaned_data.get("website")
            if selected_website:
                directory_path = selected_website
                directory_path = f'output/website_content/{directory_path}'
                directory_path = directory_path.replace('https://', '')

                run_text_process(directory_path)  # اجرای اسکریپت پردازش متن

                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
    else:
        form = SelectWebsiteForm(user)

    return render(request, 'userpanel/remove1.html', {'form': form})


@login_required
def create_content_website(request):
    if request.method == 'POST':
        form = ContentWebsiteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'userpanel/create_content_website.html',
                          {'form': form, 'success_message':
                              'Content created successfully!'})
    else:
        form = ContentWebsiteForm()
    return render(request, 'userpanel/create_content_website.html',
                  {'form': form})


@login_required
def process_dots_text(request):
    user = request.user
    if request.method == 'POST':
        form = SelectWebsiteForm(user, request.POST)
        if form.is_valid():
            if SelectWebsiteForm:
                selected_website = form.cleaned_data.get("website")
                target_directory = f'output/website_content/{selected_website}'
                target_directory = target_directory.replace('https://', '')
                process_directory_dots_text(target_directory)

                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
    else:
        form = SelectWebsiteForm(user)
    return render(request, 'userpanel/process_dots.html', {'form': form})


@login_required
def update_wordpress(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            instance = form.save()
            wordpress_url = instance.wordpress_url
            username = instance.username
            password = instance.password
            content_folder = instance.content_folder

            for filename in os.listdir(content_folder):
                if filename.endswith('.txt'):
                    post_id = filename[:-4]
                    with open(os.path.join(content_folder, filename), 'r',
                              encoding='utf-8') as file:
                        content = file.read()
                        update_result = update_post_content(wordpress_url,
                                                            username, password,
                                                            post_id, content,
                                                            publish=True)
                        if update_result:
                            print(
                                f"Post {post_id} updated and published successfully.")
                        else:
                            print(
                                f"Failed to update and publish post {post_id}.")

                    time.sleep(120)
    else:
        form = WebsiteForm()
    return render(request, 'userpanel/update_form.html', {'form': form})


def temp1(request):
    content_list = ContentWebsite.objects.all()
    content_data = []
    for content in content_list:
        content_data.append({
            'title': content.title,
            'content': content.content,
            'post_id': content.post_id,
        })
    return render(request, 'userpanel/temp1.html', {'content_data': content_data})


@login_required
def fetch_content2(request):
    if request.method == 'POST':
        website_id = request.POST.get('website_id')
        website_url = request.POST.get('website_url')
        wordpress_username = request.POST.get('wordpress_username')
        wordpress_password = request.POST.get('wordpress_password')

        batch_size = 1000  # تعداد پست‌ها در هر گروه
        output_directory = f"output/website_content/{website_url}"  # دایرکتوری خروجی
        output_directory = output_directory.replace('https://', '')
        # اجرای اسکریپت با اطلاعات دریافتی و پارامترهای بقیه
        success = get_wordpress_posts(
            website_url, wordpress_username, wordpress_password,
            start_post=1, batch_size=batch_size, website_id=website_id
        )

        if success:
            messages.success(request, "محتوا با موفقیت دریافت شد.")
            return redirect('add_phrase')
        else:
            messages.error(request,
                           "موفقیت‌آمیز نبود. لطفاً دوباره امتحان کنید.")
            return redirect('add_phrase')

    else:
        return JsonResponse({'success': False})






def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(
                'user_panel')  # یا هر صفحه‌ای که بعد از ورود به آن هدایت می‌شود
        else:
            error_message = "نام کاربری یا رمز عبور اشتباه است."
            return render(request, 'userpanel/login.html',
                          {'error_message': error_message})

    if request.user.is_authenticated:
        return redirect(
            'user_panel')  # هدایت به صفحه‌ای دیگر اگر کاربر لاگین کرده است
    return render(request, 'userpanel/login.html')


def custom_logout(request):
    logout(request)
    return redirect('custom_login')


def update_profile(request, user_id):
    user = get_object_or_404(User, pk= user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('userpanel/profile.html', user_id=user.id)
    else:
        # Handle case where first_name or last_name is empty
        pass

    return render(request, 'userpanel/update_profile.html', {'user': user})


def update_website(request, website_id):
    website = get_object_or_404(Website, pk=website_id)
    contents = ContentWebsite.objects.filter(website=website_id)
    return render(request, 'userpanel/update_website.html', {'website': website, 'contents': contents })