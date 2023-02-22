from typing import Union

import requests
from django.shortcuts import render
from django.utils.datetime_safe import datetime

from .models import *
from .forms import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from markdownx.utils import markdownify
from django.contrib import messages

from django.core.files.storage import FileSystemStorage


# Create your views here.
def home(request):
    giveaways = GiftModelUserEntry.objects.all()
    # context = {
    #     'giveaway': giveaways,
    # }
    auto_giveaways = automatic_scrape(5)
    print('77777ere77777 ', auto_giveaways)
    return render(request, 'auto_scraping/index.html', {'giveaways':giveaways,
                                                        'auto_giveaways':auto_giveaways})


def create_number_of_initial_autoscrapping_items():
    pass


def automatic_scrape(number_of_items: int = 5):
    auto_giveaways = GiftModelAutoScraping.objects.all()
    # context = {'auto_giveaways': auto_giveaways}


    api_key = 'AIzaSyCAeJSWUnOjrYg64Baa96mx7xlHeOKSkaY'
    from datetime import datetime, timezone, timedelta
    from apiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=api_key)
    published_after_date = (datetime.now(timezone.utc) - timedelta(
        days=6)).isoformat().replace("+00:00", "Z")
    request = youtube.search().list(q='Giveaway', part='snippet', type='video',
                                    publishedAfter=published_after_date,
                                    order='viewCount',
                                    regionCode='US',
                                    )
    res = request.execute()
    from pprint import PrettyPrinter
    pp = PrettyPrinter()

    pp.pprint(res)

    auto_scraping_object = GiftModelAutoScraping.objects.all()
    # auto_scraping_object = get_object_or_404(GiftModelAutoScraping, id=1)

    print('999999999999999999 ', auto_scraping_object)
    create_number_of_initial_autoscrapping_items()
    for count, video in enumerate(res.get('items')):
        print('zzzzzzzzzzzzzzz ', video.get('id').get('videoId'))
        auto_scraping_object, created = GiftModelAutoScraping.objects.get_or_create(
            id=count)
        print('7777777777 ', auto_scraping_object, '000000000000000 ', created)
        # auto_scraping_object = GiftModelAutoScraping.objects.all()

        auto_scraping_object.gift_name = video.get('snippet').get('title')
        auto_scraping_object.thumbnail_link = video.get('snippet').get('thumbnails').get('default').get('url')
        auto_scraping_object.time = video.get('snippet').get('publishedAt')
        auto_scraping_object.link = 'https://www.youtube.com/watch?v='\
                                    +video.get('id').get('videoId')
        auto_scraping_object.save()

    return auto_giveaways




def scheduled_update_for_auto_scraping():
    pass

def detail(request, id):
    giveaway = get_object_or_404(GiftModelUserEntry, id=id)
    giveaway.ingredients = markdownify(giveaway.link)
    giveaway.directions = markdownify(giveaway.username)

    # context = {
    #     'giveaway': giveaway,
    # }
    return render(request, 'auto_scraping/detail.html', {'giveaway': giveaway})


def validate_link(url: str) -> Union[dict, bool]:
    # url = url.split('&')[0]
    thumbnail_url = f'https://img.youtube.com/vi/{url}/default.jpg'
    thumbnail_url = f'https://img.youtube.com/vi/{url}/default.jpg'
    if 'www.youtube.com/watch?v=' in url:
        url = url.split('&')[0]
        thumbnail_url = url.split('v=')[1]
        thumbnail_url = f'https://img.youtube.com/vi/{thumbnail_url}/default.jpg'
        return False if requests.get(thumbnail_url).status_code != 200 else {\
            'url':url,\
            'thumbnail_url':thumbnail_url, 'link_valid':True}  #
    return False




@login_required
def create(request):
    context = {}
    if request.method == 'GET':
        form = GiftModelUserForm()
        context = {}
        context['form'] = GiftModelUserForm()
        return render(request, 'auto_scraping/create.html', context)
    elif request.method == 'POST':
        form = GiftModelUserForm(request.POST)
        print('8888888888',validate_link(form['link'].value()))
        link_check_result = validate_link(form['link'].value())
        if link_check_result is False:
            messages.error(request, 'Please enter a valid youtube link')
            print('6666666666666')
            form = GiftModelUserForm()
            context = {}
            context['form'] = GiftModelUserForm(request.POST)
            storage = messages.get_messages(request)
            storage.used = True
            return render(request, 'auto_scraping/create.html', context)


        if GiftModelUserEntry.objects.all().filter(link=form['link'].value(
        )).exists():
            messages.warning(request, 'Url already added. You can try to '
                                      'add a new Url')

            form = GiftModelUserForm()
            context = {}
            context['form'] = GiftModelUserForm(request.POST)
            return render(request, 'auto_scraping/create.html', context)
        else:
            if form.is_valid():
                print('aaaaaaaaaaaaaaaaaa ', link_check_result)
                url, thumbnail_url, link_valid = link_check_result
                url = form['link'].value().split('v=')[1]
                thumbnail_url = f'https://img.youtube.com/vi/{url}/default.jpg'
                new = GiftModelUserEntry()
                new.username = request.user
                new.link = form['link'].value()
                new.thumbnail_link = thumbnail_url
                new.gift_name = form['gift_name'].value()
                new.save()
                # form.save()
                return redirect('home')
            else:
                context['form'] = GiftModelUserForm()
                return render(request, 'auto_scraping/create.html', context)
    return render(request, 'auto_scraping/create.html', context)





@login_required
def delete(request, id):
    recipe = get_object_or_404(GiftModelUserEntry, id=id)
    if not request.user == recipe.author:
        return redirect('detail', recipe.id)
    else:
        name = recipe.name
        recipe.delete()
        context = {
            'name': name
        }
        return render(request, 'app/delete.html', context)
