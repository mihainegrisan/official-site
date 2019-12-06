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
[x] - make images added through url responsive
[x] - markdown preview in templates
[x] - make your own markdown preview
[x] - bug in the models - how long does it take to read a post
[x] - !bug - code snippets not rendering correctly in templates

[ ] - remove all features that a blog doesn't need
[---] - similar posts feature (widget)
[---] - latest posts feature (widget)
[---] - popular tags (picture on my phone) (widget)

[ ] - sending asynchronous emails in production (to a list of subscribers)
[!] - SameOrigin=Strict header  - middleware not working
[ ] - add markdown preview in admin
[ ] - own comments on site
[ ] - subscribe feature (receive emails when new posts are published)
[ ] - add feature to be able to 'schedule' a post. The users should not be able to see them. (SelectDateWidget)
[ ] - add the draft feature when a user makes a new post and let only the author see it.
[ ] -
[ ] -
[ ] - button to view the post_detail for each post ?
[ ] - RSS feed ?
[ ] - git branches

CSS:
[x] - hide sidebar for xs, sm and md screens
[x] - make badges for tags
[x] - make badges for time_to_read
[x] - make nav link active when you're on the specific page(except on login)
[x] - fix menu background on small screens
[x] - change buttons styles (override bootstrap btn-outline-primary)
[x] - add google material design to the side content
[ ] - change the main card of post_list, post_detail all of them to material design
[ ] - add underline animation to navbar links



CV app (mostly front-end bootstrap 4):
[ ] - create cv app
[ ] - create home template
[ ] - link to the blog
[ ] -
[ ] -
[ ] -



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
[ ] - block IP addresses
[ ] - authentication with email address OR username AND password
[ ] - add Google's two factor authentication https://github.com/Bouke/django-two-factor-auth
[ ] -
[ ] -
[ ] -
