1. python==3.8.10

2. Large TemporaryMemory python object are not serializeable by CELERY.
    CCEXTRACTOR does not accepts python FILE-objects as -STDIN.
    Therefore, Temporarily save VIDEO-FILE locally and delete it, when processed.

3. In Non-DEBUG mode django does not serve static files insted the request is 
    redirected to AWS-S3 bucket server which sends the file directly to the 
    browser, so no saperate server is required for static files.

4. Remove STATICFILES_STORAGE from settings when testing static-files locally.


