Blog app:
[x] - create blog app
[x] - create Post model
[x] - create custom Manager ('published')
[x] - tags for posts
[x] - create profile when a new user is created (view -> login_required)
[x] - CRUD functionality
[x] - serve images from AWS S3 Bucket
[x] - update get_absolute_url() with slug and date_posted(year, month, day)
[x] - display time to read a particular blog post
[x] - share a blog post via email
[ ] - !? linking with get_absolute_url(year, .. slug) instead of '{% url %} id' (post_share, PostUpdateView and PostDeleteView + urls paths)
[x] - refactor from class-based view to function-based view to implement the next two ...
[x] - deal with InvalidPage exceptions (PageNotAnInteger, EmptyPage)
[x] - query posts by tag
[x] - comments for FB + likes
[x] - search post feature (make sure it works with pagination)
[---] - markdown preview in admin and/or front-end
[ ] - make suggestions for similar posts
[ ] - my own comments on site
[ ] - query the latest posts and display them
[ ] - button to view the post_detail each post ?
[ ] - subscribe feature to receive emails when new posts are published
[ ] - add feature to be able to 'schedule' a post. The users should not be able to see them. (SelectDateWidget)
[ ] - add the draft feature when a user makes a new post and let only the author see it.
[ ] -
[ ] -
[ ] - git branches


Users app:
[x] - create users app
[x] - create Profile model
[x] - password reset functionality (templates)
[x] - register
[x] - login
[x] - logout
[ ] -
[ ] -


Miscellaneous:
[x] - split settings (base, dev, prod)
[x] - create GitHub repository
[x] - create core app (py manage.py rename old_project_name new_project_name) - custom command
[x] - generate xml sitemap file (add and install sites and sitemap)
[x] - honeypot and change admin/ route + environ var for the url
[x] - change home.html name to post_list.html and all related files
[x] - split some blocks of code into different templates (ex. pagination)
[x] - customize Admin ()
[ ] - RSS feed
[ ] - block IP addresses
[ ] - authentication with email address OR username AND password
[ ] - add Google's two factor authentication https://github.com/Bouke/django-two-factor-auth
[ ] -
[ ] -
[ ] -
