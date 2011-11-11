import urllib2, simplejson, sys, urllib
from datetime import datetime

HOST = 'http://api.twitter.com:80'
FRIENDS = '/1/friends/ids.json'
LOOKUP_USERS = '/1/users/lookup.json'

def make_request(url, params):
    #qs = '&'.join([x+'='+y for x,y in params.iteritems()])
    qs = urllib.urlencode(params)
    url = url+"?"+qs
    #print url
    try:
        resp = urllib2.urlopen(url)
    except:
        print 'no results'
        return None

    if not resp.getcode() == 200:
        print resp.getcode()
        return None
    result = resp.read()
    data = simplejson.loads(result)
    resp.close()
    return data

def lookup_users(users):
    result = make_request(HOST+LOOKUP_USERS, {'user_id': users, 'included_entities': True})
    return result

def get_friends(user):
    result = make_request(HOST+FRIENDS, {'cursor': '-1', 'screen_name':user})
    if not result:
        return None

    friends = []
    ids = result['ids']
    for i in range(0, len(ids), 100):
        friends.extend(lookup_users(ids[i:i+100]))
    return friends

friends = get_friends(sys.argv[1])

top = []
for friend in friends:
    count = friend['statuses_count']
    start = friend['created_at']
    # format: Tue Mar 21 20:50:14 +0000 2006
    t = datetime.strptime(start, '%a %b %d %H:%M:%S +0000 %Y')
    top.append( (friend['screen_name'], float(count)/(datetime.now() - t).days) )

# print 25 ten by tweets per day
for t in sorted(top, key=lambda x: x[1], reverse=True)[:25]:
    print t

