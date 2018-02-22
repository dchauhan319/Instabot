import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
BASE_URL = 'https://api.instagram.com/v1/'

def owner_info():
    r=requests.get("%susers/self/?access_token=%s"%(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print 'Username: %s' % (r['data']['username'])
        print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])
    else:
        print "wrong information"

def owner_recent_post():
    r=requests.get("%susers/self/media/recent/?access_token=%s"%(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        if len(r['data'])>0:
            name = r['data'][0]['id'] + ".jpg"
            url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(url,name)
            print "Image downloaded"
        else :
            print "No. post to show"
    else:
        print "wrong information"

def get_user_id(username):
    r =requests.get("%susers/search?q=%s&access_token=%s" %(BASE_URL,username,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        return r['data'][0]['id']
    else:
        print "User not available"

def get_user_info(user_name):
    user_id = get_user_id(user_name)
    r = requests.get("%susers/%s/?access_token=%s" % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print 'Username: %s' % (r['data']['username'])
        print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])
    else:
        print "wrong information"

def get_media_id(user_name):
    uid = get_user_id(user_name)
    r = requests.get("%susers/%s/media/recent/?access_token=%s" %(BASE_URL, uid, APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        if len(r['data'])>0:
            return r['data'][0]['id']
        else:
            print "No post to show"

    else:
        print "error"


def like_a_post(user_name):
    media_id = get_media_id(user_name)
    url = (BASE_URL + 'media/%s/likes')%(media_id)
    payload = {"access_token":APP_ACCESS_TOKEN}
    print 'POST request url : %s' %(url)
    r = requests.post(url,payload).json()
    if r['meta']['code']==200:
        print 'like successful'
    else:
        print 'like unsuccessful'


def comment_on_post(user_name):
    media_id = get_media_id(user_name)
    comment = raw_input("What is your comment")
    url = (BASE_URL + 'media/%s/comments') %(media_id)
    payload = {"access_token":APP_ACCESS_TOKEN, 'text': comment}
    print 'POST request url : %s' %(url)
    r = requests.post(url,payload).json()
    if r['meta']['code']==200:
        print 'comment successful'
    else:
        print 'comment unsuccessful'


def delete_post(user_name):
    media_id = get_media_id(user_name)
    r = requests.get("%smedia/%s/comments?access_token=%s" % (BASE_URL,media_id, APP_ACCESS_TOKEN)).json()
    for i in range(0,len(r['data'])):
        comment_id = r['data'][i]['id']
        comment_text = r['data'][i]['text']
        blob = TextBlob(comment_text,analyzer=NaiveBayesAnalyzer())
        if blob.sentiment.p_negative > blob.sentiment.p_positive:
            r = requests.delete("%smedia/%s/comments/%s?access_token=%s" %(BASE_URL,media_id,comment_id,APP_ACCESS_TOKEN)).json()
            print 'Comment deleted'
        else:
            print 'Comment is positive'



def get_user_post(user_name):
    user_id = get_user_id(user_name)
    r = requests.get("%susers/%s/media/recent/?access_token=%s" % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        if len(r['data']) > 0:
            name = r['data'][0]['id'] + ".jpg"
            url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(url, name)
            print "Image downloaded"
        else:
            print "No. post to show"
    else:
        print "wrong information"

while True:
    question = input("What do you want to do? \n 1. Get Owner Info \n 2. Get recent posts of Owner \n 3. Get other user info \n 4. Get other user recent post \n 5. like a post \n 6. Comment a post \n 7. Delete a comment \n 0. Exit \n ")
    if question==1:
        owner_info()
    elif question==2:
        owner_recent_post()
    elif question==3:
        user_name=raw_input("What is the username of the user")
        get_user_info(user_name)
    elif question==4:
        user_name = raw_input("What is the username of the user")
        get_user_post(user_name)
    elif question==5:
        user_name = raw_input("What is the username of the user")
        like_a_post(user_name)
    elif question==6:
        user_name = raw_input("What is the username of the user ")
        comment_on_post(user_name)
    elif question==7:
        user_name = raw_input("What is the username of the user")
        delete_post(user_name)
    elif question==0:
        exit()
    else:
        print "wrong input"