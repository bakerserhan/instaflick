# coding=utf-8
from flask import render_template, redirect, url_for, request
from instaflick import app
from instagram.client import InstagramAPI
import flickrapi
from . import settings
from random import choice

@app.route('/')
def home():
    return '''Search for your query as domain/i/query for searching from Instagram  or  domain/f/query for searching from Flickr
    <br/><br/>Flickr search results might be retrieved a bit slow.
           '''

@app.route('/i/<insta_query>')
def instagram(insta_query):
    INSTA_CLIENT_ID = ENV['INSTA_CLIENT_ID']
    INSTA_CLIENT_SECRET = ENV['INSTA_CLIENT_SECRET']

    urlList_instagram = []
    api = InstagramAPI(INSTA_CLIENT_ID, INSTA_CLIENT_SECRET)  # authenticate

    # github.com/Instagram/python-instagram/blob/master/instagram/client.py#L146
    tag_recent = api.tag_recent_media(count=20, tag_name=insta_query)

    for media in tag_recent[0]:  # tuple's first index
        urlList_instagram.append(media.images['standard_resolution'].url)
        #print "created-", media.created_time
        #print "id------", media.id
        #print "user----", media.user
        #print "name----", media.user.username
        #print "likes---", media.like_count
        #print "likers--", media.likes
        #if hasattr(media, 'tags'):
            #print "tags----", media.tags
        #print '\n'
    return "<img src="+choice(urlList_instagram)+">"


@app.route('/f/<flickr_query>')
def flickr(flickr_query):
    FLICKR_API_KEY = ENV['FLICKR_API_KEY']
    flickr = flickrapi.FlickrAPI(FLICKR_API_KEY)
    photos = flickr.photos_search(
        tags=flickr_query, per_page=15, sort='interestingness-desc')

    photo_iter = photos.iter('photo')
    i = 0
    urlList_flickr = []
    for photo in photo_iter:
        # get the photo id
        id = photo.attrib['id']
        # get the different sizes of photo
        sizes_element = flickr.photos_getSizes(photo_id=id)
        # interator for sizes
        sizes_iter = sizes_element.iter('size')
        # iterate over the sizes
        for size in sizes_iter:
            # check its size
            if size.attrib['label'] == 'Original':
                urlList_flickr.append(size.attrib['source'])
    return "<img src="+choice(urlList_flickr)+" width=""600px"">"

