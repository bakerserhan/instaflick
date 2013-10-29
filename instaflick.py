from instagram.client import InstagramAPI
import flickrapi
import settings
from random import choice

def get_from_instagram(search_term):
    insta_client_id = settings.insta_client_id
    insta_client_secret = settings.insta_client_secret

    urlList_instagram = []
    api = InstagramAPI(insta_client_id, insta_client_secret)  # authenticate

    # github.com/Instagram/python-instagram/blob/master/instagram/client.py#L146
    tag_recent = api.tag_recent_media(count=20, tag_name=search_term)

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
    return choice(urlList_instagram)

def get_from_flickr(search_term):
    flickr_api_key = settings.flickr_app_key
    flickr = flickrapi.FlickrAPI(flickr_api_key)
    photos = flickr.photos_search(
        tags=search_term, per_page=15, sort='interestingness-desc')

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

    return choice(urlList_flickr)

def main():
    search_term = raw_input()
    instagram_url = get_from_instagram(search_term)
    flickr_url = get_from_flickr(search_term)
    print instagram_url + '\n' + flickr_url

if __name__ == '__main__':
    main()
