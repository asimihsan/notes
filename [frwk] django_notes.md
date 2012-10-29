# Django notes

## Tutorial

### Part 1

-	`django-admin.py startproject mysite`
-	`python manage.py runserver 0.0.0.0:8000`
-	Edit `settings.py`
	-	Update database engine.
	-	Update timezone.
	-	Update `INSTALLED_APPS`
-	`python manage.py syncdb`
	-	Create tables required for `INSTALLED_APPS` in `settings.py`
-	`python manage.py startapp polls`
-	Models are DRY. Definitive source of data model, derive from it.
-	`vim polls\models.py`
	-	Add `__unicode__()` methods to models! Not `__str__()`!
-	`python manage.py sql polls`
	-	Shows you what SQL commands will be used to set up scheme for the application.
-	`python manage.py validate`
	-	Check models for errors.
-	`python manage.py sqlcustom polls`
	-	Print custom SQL commands for app.
-	`python manage.py sqlclear polls`
	-	SQL commands to drop the tables for an app
-	`python manage.py sqlindexes poll`
	-	SQL commands to create indexes.
-	`python manage.py sqlall polls`
	-	All SQL commands (sql, sqlcustom, sqlindexes)
-	`python manage.py shell`
	-	Pops open IPython for your project.

### Part 2

-	Admin site is for content managers, not the public.
-	Uncomment `django.contrib.admin` in `INSTALLED_APPS`, then run `python manage.py syncdb`
-	Uncomment admin lines in `mysite/urls.py`
-	Need to create `admin.py` in each app directory we want to have admin functionality for.
-	Each `admin.py` file can define custom admin views via a `ModelAdmin` derived objected.
-	Can also edit `list_display` to change how objects are listed in admin page.
-	`inlines` to put child objects in-line with the parent.
-	Add custom fields to your model to change how admin page shows it (`admin_order_field`, `boolean`, `short_description`)
-	Add `list_filter` to object admin object to allow one to filter by it.
-	Add `search_fields` to add a search box
-	Add `date_hierarchy` to add hierarchical navigation
-	`settings.py` -> `TEMPLATE_DIRS` specifies hierarchy of template directories to search in. Can copy `base_site.html` from `django/contrib/admin/templates` to `TEMPLATE_DIR/admin/base_site.html` to customise the admin template.

### Part 3

-	`settings.py` -> `ROOT_URLCONF` indicates what file does URL routing.
-	default for now: `mysite/urls.py`
-	pattern: `(regular expression, Python callback [, optional dictionary])`. Calls callback with an `HttpRequest` object as the first argument, captured values as keyword args, and dict as optional keyword args (e.g. `polls.views.index`)
-	Add methods to `mysite/views.py` for each callback
-	`render_to_response` is a shortcut to using a `loader` to load a template, using a `Context` to package up data, then returning `HttpResponse(loader.render(context))`.
	-	`from django.shortcuts import render_to_response`
-	`from django.shortcuts import get_object_or_404`
-	Can do `include` from a URLconf to put URL config into app directories, and then reference them using include from the project.

### Part 4

-	In order to use `{% csrf_token %}` in a template we need to pass `context_instance = RequestContext(request)` into the context, using `from django.template import RequestContext`
-	Always return `HttpResponseRedirect` after successful POST to prevent double submits if user hits back.
-	Use generic views to avoid boilerplate for "get from DB -> render -> return" pattern. (ListView, DetailView)

## Heroku notes

-    Setting up on Heroku: https://devcenter.heroku.com/articles/django

        heroku create
        git push heroku master
        heroku ps:scale web=1
        
        # check status
        heroku ps
        
        # open browser
        heroku open
        
        # check logs
        heroku logs
        
        # restart
        heroku ps:restart web
        
        # run one-offs, even interactive
        heroku run python manage.py syncdb
        heroku run python manager.py shell
        
-    Should use gunicorn
    -    `pip install gunicorn`
    -    Add 'gunicorn' to `INSTALLED_APPS`
    -    Create a Profile with:
    
            web: gunicorn canihazmusic.wsgi -b 0.0.0.0:$PORT
            
    -    To run locally:
    
            foreman start
            
    -    To deploy, commit and push `Procfile`, `requirements.txt`, `settings.py`, then:
        
            git push heroku master

-    Can set up celery background workers as well.
-    If you want static files to work (you do):

        PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        
        # this is the output dir where statics are collected
        STATIC_ROOT = os.path.join(PROJECT_DIR, "staticfiles") 
        
        # this is the input
        STATICFILES_DIRS = (os.path.join(PROJECT_DIR, "static"), )

        # how to collect, heroku does this for you
        ./manage.py collectstatic


## Using Django

### Models and databases

-	Models have fields.
-	Fields have optional arguments, notably: null, blank, choices (combo box), default, help_text, primary_key, unique
-	Relationships
	-	Many-to-one (e.g. Car->Manufacturer). => ForeignKey on Car to Manufacturer.
	-	Many-to-many (e.g. Pizza->Toppings). => ManyToManyField on Pizza to Topping.
		-	When you want to associate per-association data use intermediary objects, i.e. a ManyToManyField with a 'through' keyword pointing at the intermediary object. Intermediary object has a pair of ForeignKey fields and associated data.
	-	One-to-one, using OneToOneField, e.g. Restaurant to Place.
-	Can create custom fields.
-	TOREAD

### User authentication

-	TODO

### Kata - image upload

-	You need the latest version of `django-storages`, or else when you open a new file for write it won't create it for you. Instead of `pip install django-storages` you want to get `https://bitbucket.org/david/django-storages/src`
-	`django-admin.py startproject imageupload`
-	`./manage.py startapp images`
-	Open `imageupload/settings.py` for editing, make the following changes:
	-	At the type use relative directory as base:
	
			import os                                                                                                                                       
			PROJECT_DIR = os.path.dirname(__file__)
			
	-	Database changes to:
	
			DATABASES = 
				'default': {
				    'ENGINE': 'django.db.backends.sqlite3',
					'NAME': os.path.join(PROJECT_DIR, "database.sqlite3")
					…
			
	-	`TIME_ZONE = 'Europe/London'`
	-	`MEDIA_ROOT = os.path.join(PROJECT_DIR, "incoming")`
	-	`STATIC_ROOT = os.path.join(PROJECT_DIR, "static")`
	-	`STATIC_URL = '/static/'`
	-	`TEMPLATE_DIRS` includes `os.path.join(PROJECT_DIR, "templates")`
	-	`INSTALLED_APPS`:
	
			INSTALLED_APPS = (
			    # Built-in contrib apps.
			    'django.contrib.auth',
			    'django.contrib.contenttypes',
			    'django.contrib.sessions',
			    'django.contrib.sites',
			    'django.contrib.messages',
			    'django.contrib.staticfiles',
			    'django.contrib.admin',
			    'django.contrib.admindocs',
			
			    # Third party apps.
			    'storages',
			
			    # Custom apps.
			    'images',
			)
	-	Settings specific to `django-storages`
		
			DEFAULT_FILE_STORAGE = r'storages.backends.s3boto.S3BotoStorage'
			AWS_STORAGE_BUCKET_NAME = r'djangokata-imageupload'

-	In the settings above we've deliberately not specified `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, and instead have put them inside `~/.boto`. Could also have specified them as environment variables `ACCESS_KEY_NAME` and `SECRET_KEY_NAME`, see `storages/backends/s3.py`.
-	Of course generate a new set of AWS IAM credentials, give them an appropriate policy, create the AWS S3 bucket.
-	For debugging purposes we set `[Boto] -> debug = 2` in `~/.boto` so that we can see AWS requests on the wire as we manipulate Django objects.
-	`chmod +x manage.py`
-	`./manage.py syncdb`
-	Make the Images model accessible via the admin page by creating `images/admin.py`:

		from images.models import Image
		from django.contrib import admin
		
		admin.site.register(Image)

-	`images/models.py`:

		from django.db import models
	
		class Image(models.Model):
		    description = models.CharField(max_length=255)
		    image = models.ImageField(upload_to='files_images')
		
		    def __unicode__(self):
		        return "{Image: description=%s, image=%s}" % (self.description, self.image)

-	Open a Django shell via `./manage.py shell` and confirm that file uploads are working.

		from django.core.files.storage import default_storage

		In [3]: i = Image(description="cute dog!")
		In [4]: i.image
		Out[4]: <ImageFieldFile: None>
		In [33]: i.image.name = "cute_dog.jpeg"
		
		In [34]: i.image.file = default_storage.open("cute_dog.jpeg", "wb")
		send: 'HEAD /cute_dog.jpeg HTTP/1.1\r\nHost: djangokata-imageupload.s3.amazonaws.com\r\nAccept-Encoding: identity\r\nDate: Mon,11 Jun 2012 20:48:29 GMT\r\nContent-Length: 0\r\nAuthorization: AWS AKIAJEMCK4EPGCYIJ5PA:OIsMEx7+1xWsrhXZbSq93hvyRt0=\r\nUser-Agent: Boto/2.4.1 (darwin)\r\n\r\n'
		reply: 'HTTP/1.1 404 Not Found\r\n'
		header: x-amz-request-id: C2EFE146464C0276
		header: x-amz-id-2:nAn60Wm8Uvb4uPHkJnRkPQMaz9sgNWQnVH6CGrdjzX1QtJCEj9RWTu7IeTQVb33d
		header: Content-Type: application/xml
		header: Transfer-Encoding: chunked
		header: Date: Mon, 11 Jun 2012 20:48:30 GMT
		header: Server: AmazonS3
		
		In [35]: contents = open("incoming/dog_shelf.jpeg", "rb").read()
		In [36]: i.image.file.write(contents)
		send: 'POST /cute_dog.jpeg?uploads HTTP/1.1\r\nHost: djangokata-imageupload.s3.amazonaws.com\r\nAccept-Encoding: identity\r\nDate: Mon, 11 Jun 2012 20:48:52 GMT\r\nContent-Length: 0\r\nx-amz-acl: public-read\r\nAuthorization: AWS AKIAJEMCK4EPGCYIJ5PA:KP/BjWI0mGjvLU7UvaajmZhfhAI=\r\nUser-Agent: Boto/2.4.1 (darwin)\r\n\r\n'
		reply: ''
		send: 'POST /cute_dog.jpeg?uploads HTTP/1.1\r\nHost: djangokata-imageupload.s3.amazonaws.com\r\nAccept-Encoding: identity\r\nDate: Mon, 11 Jun 2012 20:48:52 GMT\r\nContent-Length: 0\r\nx-amz-acl: public-read\r\nAuthorization: AWS AKIAJEMCK4EPGCYIJ5PA:KP/BjWI0mGjvLU7UvaajmZhfhAI=\r\nUser-Agent: Boto/2.4.1 (darwin)\r\n\r\n'
		reply: 'HTTP/1.1 200 OK\r\n'
		header: x-amz-id-2: QXF5YRBoLimRdX7HW8TgEirS9FwXSP+pkEcWIOrtDcASaCA9BEXn34ZRQaxs959q
		header: x-amz-request-id: 1957DB4B06924EE3
		header: Date: Mon, 11 Jun 2012 20:48:54 GMT
		header: Transfer-Encoding: chunked
		header: Server: AmazonS3
		
		In [37]: i.image.file.close()
		send: u'PUT /cute_dog.jpeg?uploadId=tX.nGrEBWqj1pqBRl8VR02PrrqYk0GHBPjosIHzlVx5..nFAFYGJE4qlbrWOM30.fqab5syorrdzstP6S5ZYahjOt3tEMzhsE6WECxGli0y2TPUvYdUt.eZpWk8u8SeA&partNumber=1 HTTP/1.1\r\nHost: djangokata-imageupload.s3.amazonaws.com\r\nAccept-Encoding: identity\r\nContent-Length: 47714\r\nContent-MD5: dMy9GogJjlqcjIpHwAlRGg==\r\nExpect: 100-Continue\r\nDate: Mon, 11 Jun 2012 20:48:58 GMT\r\nUser-Agent: Boto/2.4.1 (darwin)\r\nContent-Type: application/octet-stream\r\nAuthorization: AWS AKIAJEMCK4EPGCYIJ5PA:jlTl+tDwnhf/0XvmmH5XdF3DT6U=\r\n\r\n'

		In [42]: i.image.url
		Out[42]: 'https://djangokata-imageupload.s3.amazonaws.com/cute_dog.jpeg?Signature=8d58N4lG%2BN47V1Z%2F1SMt7%2Fh2JaA%3D&Expires=1339451530&AWSAccessKeyId=AKIAJEMCK4EPGCYIJ5PA'
		
		In [43]: i.save()

-	Note that the S3 gets (`i.image.url`) are HMAC signed against your AWS IAM credentials. If you prevent public access to your S3 bucket and allow your credentials access then you need a valid signature in order to access your S3 objects. To demonstrate, attempt to HTTP GET the URL with and without the HTTP GET arguments.
-	These signatures are not static. They get regenerated by Boto every time we request the field:

		In [48]: from images.models import Image
		In [49]: Image.objects.all()[0].image.url
		Out[49]: 'https://djangokata-imageupload.s3.amazonaws.com/cute_dog.jpeg?Signature=m3g4WDG%2Bmk6G5SNxBE%2FBGo4phMo%3D&Expires=1339453552&AWSAccessKeyId=AKIAJEMCK4EPGCYIJ5PA'

-	TODO Deleting an object doesn't delete the actual S3 object, this is by design. Fix is to either override the `save()` method on the model, to hook into a signal, or to perform cron-triggered reaping in the background for orphaned files.


## Practical Django Projects

### Your First Django site: a Simple CMS

-	You can have per-app template overrides.
-	If you have a per-app override for an admin template, admin searches e.g.
	-	`admin/flatpages/flatpage/change_form.html`
	-	`admin/flatpages/change_form.html`
	-	`admin/change_form.html`
-	Hence you can specify a per-model override of the admin change page to e.g. include TinyMCE (p24).
-	Cheeky search e.g.: `results = ModelObject.objects.filter(content__icontains=string)`
-	Models typically implement `get_absolute_url()`
-	You can access argument-less model functions in a template with `{{ model.fn }}`, note no brackets. Can't call functions with arguments.
-	Django `QuerySet`s are lazy; only executed when you attempt to get result.

### A Django-Powered Weblog

-	Can use `models.permalink` decorator for `get_absolute_url()`. See _Practical Django Projects_ page 74. This uses the URLconf for the app. (?).
-	`django.utils.encoding.smart_str()` is a cleverer version of the `str()` built-in, and returns UTF-8 rather than ASCII.

## Django Design Patterns

### URLs

-	Name all your URLs, then call them in templates as `{% url urlpatternname %}`
-	Naming scheme is `appname_viewname`, or `appname_viewname_use`

### Templates

-	One base.html at the project level, `project/templates/base.html`
-	One base.html per app level which extends the project base.html, `project/templates/app/base.html`
-	Each template extends the app-level template, `project/template/app/custom.html`

## General notes

-	Setting up using virtualenv
	-	For your main Python installation, set it up:
	
			pip install virtualenv virtualenvwrapper
			virtualenvwrapper.sh
			cd newdir
			virtualenv env
			# if mac and homebrew alter the shebang in virtualenv to /usr/local/bin/python
			source env/bin/activate
			echo env/ >> .gitignore
			pip install django django-debug-toolbar django-uuidfield requests nose ipython ipdb boto pil gunicorn selenium South
			pip install hg+https://bitbucket.org/david/django-storages#egg=storages
			pip freeze > requirements.txt
			# deactivate to leave the vent
			
-	Gotcha. To get development static file serving working, you must copy static files somewhere, add it to the `settings.py` `STATICFILES_DIRS`, and then run `./manage.py collectstatic`. 

-	Starting off with South:
	-	`./manage.py syncdb`
	-	`./manage.py convert_to_south apps.accounts`
	-	`./manage.py convert_to_south apps.images`
	-	`./manage.py convert_to_south apps.guides`
	-	do some changes to models…
	-	`./manage.py schemamigration <app_name> --auto`
	
-	Admin config: [https://docs.djangoproject.com/en/1.4/ref/contrib/admin/](https://docs.djangoproject.com/en/1.4/ref/contrib/admin/)	
-	To view an `editable = False` field in the Django admin use `readonly_fields` in `ModelAdmin` derived class in `admin.py`.
-	`list_display` attribute on `ModelAdmin` object for list of attributes or one-parameter callables called with instance of object, returns string. Makes list of objects in admin easy to view.
-	`list_filter` for filtering by any field.
-	`search_fields` is list of fields to search over using OR. Can dereference e.g. `account__user__username`.

-	Override LiveServerTestCase's setUp() to not only launch a server thread but a RabbitMQ thread, then use Celery to put tasks onto it. Delicious!

## Django, Celery, Message Queues, Search

-	References:
	-	[http://www.slideshare.net/idangazit/an-introduction-to-celery](http://www.slideshare.net/idangazit/an-introduction-to-celery)
	-	[http://blogs.digitar.com/jjww/2009/01/rabbits-and-warrens/](http://blogs.digitar.com/jjww/2009/01/rabbits-and-warrens/)
	-	[http://www.rabbitmq.com/tutorials](http://www.rabbitmq.com/tutorials)
	-	[http://www.slideshare.net/simon/advanced-aspects-of-the-django-ecosystem-haystack-celery-fabric](http://www.slideshare.net/simon/advanced-aspects-of-the-django-ecosystem-haystack-celery-fabric)
	-	[http://www.slideshare.net/DaveSyer/syer-amqps2gx2011](http://www.slideshare.net/DaveSyer/syer-amqps2gx2011)
	-	[http://pypi.python.org/pypi/django-celery](http://pypi.python.org/pypi/django-celery)
	-	[http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)

-	Celery talks Carrot to an AMQP broker (e.g. RabbitMQ).
-	Kombu is a library to talk AMQP.
-	RabbitMQ tutorial (part 1)
	-	Use `pika`.
	-	Make a connection:
	
			connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
			channel = connection.channel()
	
	-	Make a queue, or else messages are silently dumped.
	
			channel.queue_declare(queue='hello')
			
	-	Always send messages to exchanges, you can't send them directly to queues.
	-	Exchange `''` is special. It's default, and we tell it what queue to send to:
	
			channel.basic_publish(exchange='',
								  routing_key='hello',
								  body='Hello World!')
			connection.close()
			
	-	To receive, do the same connection and queue declaration setup.
	-	(We make the queue again to avoid a race condition of producer vs consumer starting first).
	-	Then define a callback:
	
			def callback(ch, method, properties, body):
				print "got: %s" % (body, )
			channel.basic_consume(callback,
								  queue='hello',
								  no_ack=True)
								  
	-	Can make the consumer block forever:
		
			channel.start_consuming()		
			
-	RabbitMQ tutorial (part 2)
	-	Round-robin is default. Workers connected to queues are in RR.
	-	Default is for consumers to send an ACK. It's OK if consumers take a long time
		(default is no timeout) but if consumer dies then message is sent to another
		consumer:
		
			def callback(ch, method, properties, body):
				…
				ch.basic_ack(delivery_tag = method.delivery_tag)
	
	-	Debug unacknowledged messages, which consume memory:
	
			sudo rabbitmqctl list_queues name messages_received messages_unacknowledged
			
	-	For durability, both queue and messages must be explicitly marked as durable:
	
			channel.queue_declare(queue='task_queue', durable=True)
			channel.basic_publish(exchange='',
								  routing_key="task_queue",
								  body=message,
								  properties=pika.BasicProperties(
								  	delivery_mode = 2, # persistent message
								  ))
	
	-	Durable messages may still be lost; if you need stronger durability need
		_transactions_.
	-	Consumer queuing (only allowed to have one outstanding task):
	
			channel.basic_qos(prefetch_count=1)
			
-	RabbitMQ tutorial (part 3)
	-	Exchange types: `direct`, `topic`, `headers`, `fanout`.
	-	`fanout` is PUB/SUB. Broadcast all received messages to all queues it knows.
	-	Producer emits logs, consumer get them if they've bound a queue to the exchange.
	
			channel.exchange_declare(exchange='logs',
									 type='fanout')
									 
	-	Debug exchanges:
	
			sudo rabbitmqctl list_exchanges
			
	-	If you want a random queue name on creation:
		
			result = channel.queue_declare()
			# result.method.queue has a random queue name
			
	-	And when the consumer disconnects the queue should get deleted:
	
			result = channel.queue_declare(exclusive=True)
			
	-	Need to connect the exchange to the queue in the consumer:
	
			channel.queue_bind(exchange='logs',
							   queue=result.method.queue)
							   
	-	Debug bindings:
			
			sudo rabbitmqctl list_bindings


-	RabbitMQ tutorial (part 4)
	-	Routing keys (subscription topics) (ignored for fanout)
	
			channel.queue_bind(exchange=exchange_name,
							    queue=queue_name,
							    routing_key='black')
	-	Use this in `direct` exchange type; send messages to queues whose "binding key"
		(routing_key on binding) is the same as the message's "routing key".
	
-	RabbitMQ tutorial (part 5)
	-	Routing based on routing key and source.
	-	Need a `topic` exchange.
	-	Routing keys and binding keys must be `a.b.c.d.e`.
	-	Star (`*`) can substitute exactly one word.
	-	Hash (`#`) can substitute zero or more words.
	-	Binding to `#` is like fanout, match everything.
	-	Binding without `*` or `#` is like direct, match exactly.
	
-	RabbitMQ tutorial (part 6)
	-	RPC, I'll ignore for now don't want RPC.

-	Setup:
	-	`brew install rabbitmq`
	-	`rabbitmq-server` to start (`--detached` to detach)
	-	`rabbitmqctl stop`, `rabbitmqctl status`, `rabbitmqctl list_queues`
	-	`rabbitmqctl add_user username password`, `rabbitmqctl list_users`
	-	`pip install django-celery`
	-	`settings.py`:
		-	Add `djcelery` to `INSTALLED_APPS`
		
				import djcelery
				djcelery.setup_loader()
				
				BROKER_URL = "amqp://username:password@localhost:5672"
				
				# Routable tasks
				
				CELERY_AMQP_EXCHANGE = "tasks"
				CELERY_AMQP_PUBLISHER_ROUTING_KEY = "task.regular"
				CELERY_AMQP_EXCHANGE_TYPE = "topic"
				CELERY_AMQP_CONSUMER_QUEUE = "foo_tasks"
				CELERY_AMQP_CONSUMER_ROUTING_KEY = "foo.#"
				
				# Cron
				CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
				
		-	without south: `./manage.py syncdb`
		-	with south: `./manage.py migrate djcelery`
		
	-	Run at least one celery worker:
		-	Docs recommend `./manage.py celery worker --loglevel=info`
		-	`./manage.py celeryd` (`--detach` for production)
		-	Has an option `MAX_TASK_PER_CHILD`
		
	-	Define tasks in `app_name/tasks.py`.
	-	Register and auto discovery, like `admin.py`.
	
			from celery.task import Task
			from celery.registery import tasks
			import datetime
			
			class FetchUserInfoTask(Task):
				def run(self, screen_name, **kwargs):
					logger = self.get_logger(**kwargs)
					logger.info("Starting request %s at %s" % (kwargs.get('task_id', ''), datetime.datetime.utcnow()))
					try:
						user = twitter.users.show(id=screen_name)
					except TwitterError:
						raise
					return user
					
			tasks.register(FetchUserInfoTask)
			
			# then
			from myapp.tasks import FetchUserInfoTask
			result = FetchUserInfoTask.delay('username')
			
			result.ready()) # true if task finished
			result.result # return value or exception
			result.get() # blocking get
			result.successful() # True/False
		
	-	You can also do:
	
			form celery.decorators import task
			
			@task
			def add(x, y):
				return x + y
	
	-	? what about overriding `__call__` and `__after_return__`?
	-	Can chain tasks.
	-	Can retry tasks:
			
			self.retry(args=(screen_name, ), kwargs=**kwargs, exc)
			
			# or
			
			@task
			def fn(arg1, arg2):
				try:
					…
				except Exception, exc:
					fn.retry(exc=exc,
							 countdown=60,
							 args=(arg1, arg2))
				
			
	-	Periodic tasks.
	
			run_every = timedelta(seconds=60)
			
	-	Retry options
	
			default_retry_delay = 5 * 60 # 5 minutes
			max_retries = 5
	
	-	Task sets (multiple tasks in parallel)
	
			from celery.task import TaskSet
			ts = TaskSet(FetchUserInfoTask, args=(
				('username', ), {},
				('username2', ), {},
			))		
			ts_result = ts.run() # or ts.apply_async()
			rv = ts.join()
			
	-	Celery has Django views for status of tasks (`celery.views`)
	
			celery.views.apply(request, task_name, *args)
			celery.views.is_task_done(request, task_id)
			celery.views.task_status(request, task_id)
			
	-	Task's can have routing keys (`routing_key = 'foo.bars'`)
	
	-	Can tell Carrot to use a database backend for a development environment.
	-	Maybe want `PicklableHttpRequest`, so can send `request` directly to a task?
	
	-	Centralized logging:
	
			import logging
			from celery.signals import after_setup_logger, after_setup_task_logger
			def after_setup_logger_handler(sender=None, logger=None,
										   loglevel=None, logfile=None,
										   format=None, colorize=None,
										   **kwds):
				handler = logging.handlers.SysLogHandler(address=('syslogserver',
												         514))
				handler.setFormatter(logging.Formatter(format))
				handler.setLevel(logging.INFO)
				logger.addHandler(handler)
				
			after_setup_logger.connect(after_setup_logger_handler)
			after_setup_task_logger.connect(after_setup_logger_handler)
	

-	Setting up haystack
	-	Define `search_indexes.py` (like `admin.py`)
	
			from haystack import indexes, site
			from models import Object
			class ObjectIndex(index.SearchIndex):
				text = indexes.CharField(document=True, model_attr='text')
				def get_queryset(self):
					return Object.objects.all()
			
			site.register(Object, ObjectIndex)
	
	-	Hook up default haystack search views.
	
			url(r'^search/', include('haystack.urls')),
	
	-	Create `search.html` template.
	
			{% for result in page.object_list %}
				{% if result.model_name == "object") %}
				<p>{% highlight result.text with request.GET.q %}</p>
				{% endif %}
			{% endfor %}
	
	-	Run `./manage.py rebuild_index`.
	
	
-	Using haystack with solr on Mac:
	-	Tested on haystack 1.2.7 and solr 3.6.0.
	-	[http://django-haystack.readthedocs.org/en/v1.2.7/tutorial.html](http://django-haystack.readthedocs.org/en/v1.2.7/tutorial.html)
	-	Follow the instructions in the tutorial, as to the haystack side, but solr is not intuitive or obvious.
	-	Name all default (i.e. document) fields as "text", as per suggestion in the tutorial.
	-	`brew install solr`
	-	`./manage.py build_solr_schema > solr_schema.xml`
	-	Open `solr_schema.xml` for editing.
	-	In the `<fields>` section, near the bottom of the file near `django_ct` field add a new field:
	
			<field name="text" type="text" indexed="true" stored="true" multiValued="false" required="true"/>
			
	-	Move `solr_schema.xml` to the following location:
	
			/usr/local/Cellar/solr/3.6.0/libexec/example/solr/conf/schema.xml
			
	-	`cd /usr/local/Cellar/solr/3.6.0/libexec/example`
	-	`java -jar start.jar`
	-	Common errors:
		-	`No field defined text`: means you didn't add text as a field.
		-	`Premature end of file`: `schema.xml` might be a 0-byte file.
		-	`Unable to find xxxx`: Did you change directory? You must.
	-	`./manage.py rebuild_index`
	-	Check both manage.py and solr output for errors.
	-	Do a search, check no errors.
	-	To execute a search from e.g. `./manage.py shell`
			
			from haystack.query import SearchQuerySet
			results = SearchQuerySet().auto_query('my search here').load_all()
			
			# gives list of SearchResult objects, which offer model and object attributes
			