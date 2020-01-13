Models:

    1. Project

    name -
    summary -
    description -
    created - date

    2. Version

    name -
    summary -
    description -
    project - ForeignKey(Project,
                        on_delete=models.CASCADE,
                        related_name='versions')
    created - date


    3. Task/Issue

    name -
    version - ForeignKey(Version,
                        on_delete=models.CASCADE,
                        related_name='tasks')
    summary -
    description -
    attachment - files ?
    author/reporter - ForeignKey to User
    assignee(to) - who the author assigned
    type - choices ( bug OR feature/upgrade)
    priority - choose from (low, medium, high)
    affects - (which version it affects)
    Labels - (or tags)
    status - NEW, OPEN, CLOSED, TO DO, RESOLVED, INVALID.
    Resolution - unresolved, ...
    created - date
    updated - date

    Sprint -
    Environment -

    4. Comment (for each issue)
        task - ForeignKey(Task,
                          on_delete=models.CASCADE,
                          related_name='comments')
        author - ForeignKey(User)
        body - models.TextField()
        created - models.DateTimeField(auto_now_add=True)
        updated - models.DateTimeField(auto_now=True)
        active - models.BooleanField(default=True)



[ ] - create app
[ ] - make Task model
[ ] - make Comment model
[ ] - display stats on the dashboard (list_view)
    warnings, issues in version/project, issues done, issues in progress, issues to-do
[ ] -
[ ] -
[ ] -
[ ] - login_required for everything !
[ ] -
[ ] - create a search
[ ] - create a filter for search
[ ] -
