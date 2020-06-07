This is a simple Django + Celery application once required as a test task by some employer. 

The task description was the following:

*Do develop a simple Django application including files to deploy*
(either Ansible or k8s configs, I chose the latter).
*uWSGI, Django, Celery, MariaDB, RabbitMQ should be used.*

*The application should provide a single page consisting of a web-form allowing to add some video file and a list of previously added and processed files.*
*A video file can be added either by direct upload using the form or by providing a link to the file. In the latter case the application should accept a link and download a file using it. For added files the application shoulg create a thumbnail (640x360) and convert the file to mpeg4 format (both operations should be asyncronious). Application page should show a list of previously added videos with their converted files or thumbnailes if video is still being processed*
