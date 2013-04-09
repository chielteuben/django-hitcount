Django-HitCount
===============

Basic app that allows you to track the number of hits/views for a particular
object.

For more information you can view comments in the source code or visit:

<http://damontimm.com/code/django-hitcount/>

What it is not
--------------

This is not meant to be a user tracking app (see: [django-tracking][1]) or a
comprehensive site traffic monitoring tool (see: Google Analytics).

It's meant to serve as a simple hit counter for chosen objects with a couple
useful features (user-agent, session, and IP tracking) and tools to help you
on your way.

Contribute
----------

I would love to make it better.  Please fork and push.  Some fun additions
might be [1] a nice graphing utility for the admin site, [2] another approach
to caputring a hit (other than jQuery), and [3] a cleanup tool that can remove
Hit objects after a certain period (cron job).

Installation:
-------------

Simplest way to formally install is to run:

    ./setup.py install

Or, you could do a PIP installation:

    pip install -e git://github.com/chielteuben/django-hitcount.git#egg=django-hitcount

Or, you can link the source to your `site-packages` directory.  This is useful
if you plan on pulling future changes and don't want to keep running
`./setup.py install`.

    cd ~/src
    git clone git://github.com/thornomad/django-hitcount.git
    sudo ln -s `pwd`/django-hitcount/hitcount `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/hitcount

Special thanks to ariddell for putting the `setup.py` package together.

[1]:http://code.google.com/p/django-tracking/


Settings (optional)
----------

There are three additional settings you can add to your settings.py file:
    HITCOUNT_KEEP_HIT_ACTIVE = {'days': 7}
    HITCOUNT_HITS_PER_IP_LIMIT = 0
    HITCOUNT_EXCLUDE_USER_GROUP = ('Editor',)

HITCOUNT_KEEP_HIT_ACTIVE: is the number of days, weeks, months, hours, etc (timedelta kwargs), that an Hit is kept ‘active’. If a Hit is ‘active’ a repeat viewing will not be counted. After the active period ends, however, a new Hit will be recorded. 

HITCOUNT_HITS_PER_IP_LIMIT: limit the number of ‘active’ hits from a single IP address. 0 means that it is unlimited.

HITCOUNT_EXCLUDE_USER_GROUP: don’t count any hits from certain logged in users. In the example above, I don’t want any of my editors inflating the total Hit count.

Usage
----------

Urls:
    from hitcount.views import update_hit_count_ajax
    urlpatterns = patterns('',
        url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    )

Template:
Be sure to have a recent version of jQuery installed.
    {% load hitcount_tags %}
    <script type="text/javascript">
        $(document).ready(function() {
            var csrf = '{{ csrf_token }}';
            {% get_hit_count_javascript for object %}
        });
    </script>

Return total hits for an object: 
    {% get_hit_count for [object] %}

Get total hits for an object as a specified variable:
    {% get_hit_count for [object] as [var] %}

Get total hits for an object over a certain time period:
    {% get_hit_count for [object] within ["days=1,minutes=30"] %}

Get total hits for an object over a certain time period as a variable:
    {% get_hit_count for [object] within ["days=1,minutes=30"] as [var] %}
