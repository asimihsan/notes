# Architecture notes

## Main lessons

-	Keep it **simple**.

## Other

-	Use [Amazon CloudFront](http://aws.amazon.com/cloudfront/) to push content to the edges of a CDN close to consumers; "intelligent" S3.
-	[Celery with Kombu](http://docs.celeryproject.org/en/latest/tutorials/clickcounter.html) fits well with Django, worth learning and deploying with.

## High Scalability

-	iDoneThis
	-	Python, Django, PostgreSQL.
	-	Django hosts both HTML view for browsers and JSON view for Backbone.js and iPhone apps.
	-	**Lucene, Solr** for full-text search.
	-	One instance. Amazon EC2 extra large.
	-	[Celery](http://celeryproject.org/) to aynchronously sending emails (probably with RabbitMQ backend).

-	Instagram
	-	Amazon ELB -> nginx -> Django.
	-	[Gunicorn](http://gunicorn.org/) as WSGI server.
	-	[Fabric](http://fabric.readthedocs.org/en/1.3.3/index.html) for deployment.
	-	PostgreSQL running as master-replica using [streaming replication](https://github.com/greg2ndQuadrant/repmgr). EBS used for snapshotting.
	-	EBS deployed with software RAID using [mdadm](http://en.wikipedia.org/wiki/Mdadm).
	-	[Vmtouch](http://hoytech.com/vmtouch/vmtouch.c) for managing data in memory.
	-	XFS as file system, for consistent snapshots on RAID arrays.
	-	[Pgbouncer](http://pgfoundry.org/projects/pgbouncer/) for pooling PostgreSQL connections.
	-	Amazon S3 for photos, Amazon Cloudfront as CDN.
	-	redis for feeds, sessions, other mappings. Many large instances in master-replica setup. EBS snapshots of replicas.
	-	Amazon Solr for geo-search API.
	-	memcached for caching.
	-	[Gearman](http://gearman.org/#introduction) as a job dispatcher. Asynchronously sharing photos, notifying real-time subscribers, feed fan-out.
	-	[Pyapns](https://github.com/samuraisam/pyapns) for Apple push notifications.
	-	[Munin](http://munin-monitoring.org/) for graphing metrics, alerts on problems with custom plugins.
	-	[Pingdom](http://pingdom.com/) for external monitoring.
	-	[PagerDuty](http://pagerduty.com/) of handling notifications of incidents.
	-	[Sentry](http://pypi.python.org/pypi/django-sentry) for Python error reporting.

-	Google and latency
	-	Prioritize request queues and network traffic.
	-	Reduce head-of-line blocking by breaking large requests into smaller requests.
	-	Rate limit activity.
	-	Defer expensive activity if you can.