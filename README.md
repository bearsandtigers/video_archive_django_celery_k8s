This is a simple Django + Celery application once required as a test task by some employer. 

The task description was the following:

*Do develop a simple Django application including files to deploy*
(either Ansible or k8s configs, I chose the latter).
*uWSGI, Django, Celery, MariaDB, RabbitMQ should be used.*

*The application should provide a single page consisting of a web-form allowing to add some video file and a list of previously added and processed files.*
*A video file can be added either by direct upload using the form or by providing a link to the file. In the latter case the application should accept a link and download a file using it. For added files the application shoulg create a thumbnail (640x360) and convert the file to mpeg4 format (both operations should be asyncronious). Application page should show a list of previously added videos with their converted files or thumbnailes if video is still being processed*

Alongside with the application code a set of K8s YAMLs is provided allowing to deploy the app from the scratch. Deployment files were tested using k3s. K3s by default goes with Traefik preinstalled so it used as an Ingress for the application.

Looking at this code please keep in mind that this is merely a test task, very simple, intentionally not production ready and serves to display in general my understanding and ability to develop and deploy simple Python applications. 

This app posseses a lot of flaws which I'm aware of and which are normal keeping in mind the nature of this task.

For example, it keeps some secrets right in the repo in secret.yaml file, it almost has no comments (thought the code is really simple and this description and explicit names of variables should be enough), it may be uses not all the power of  Django and doesnt follow the best practices, etc, etc.
