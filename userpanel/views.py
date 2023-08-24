import time

from django.contrib.messages import success
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Website
from .forms import WebsiteForm, ReplacePhraseForm, SelectWebsiteForm, \
    ContentWebsiteForm, ProcessDotsTextForm
from django.contrib.auth.decorators import login_required
from .scripts.main import get_wordpress_posts
from .scripts.links_process import main_script
from django.contrib import messages
from .scripts.remove import run_text_process
from .scripts.update import *
from .scripts.process_dot import *


def dashboard(request):
    return render(request, 'userpanel/dashboard.html')


@login_required
def user_panel(request):
    user_websites = Website.objects.filter(user=request.user)
    return render(request, 'userpanel/user_panel.html',
                  {'user_websites': user_websites})


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


def fetch_content(request):
    if request.method == 'POST':
        website_url = request.POST.get('website_url')
        wordpress_username = request.POST.get('wordpress_username')
        wordpress_password = request.POST.get('wordpress_password')

        batch_size = 100  # تعداد پست‌ها در هر گروه
        output_directory = f"output/website_content/{website_url}"  # دایرکتوری خروجی
        output_directory = output_directory.replace('https://', '')
        # اجرای اسکریپت با اطلاعات دریافتی و پارامترهای بقیه
        success = get_wordpress_posts(
            website_url, wordpress_username, wordpress_password,
            start_post=1, batch_size=batch_size,
            output_directory=output_directory
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


def process(request):
    return render(request, 'userpanel/process.html')


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

    return render(request, 'userpanel/remove.html', {'form': form})


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
                        update_result = update_post_content(wordpress_url, username, password, post_id, content, publish=True)
                        if update_result:
                            print(f"Post {post_id} updated and published successfully.")
                        else:
                            print(f"Failed to update and publish post {post_id}.")

                    time.sleep(120)
    else:
        form = WebsiteForm()
    return render(request, 'userpanel/update_form.html', {'form': form})