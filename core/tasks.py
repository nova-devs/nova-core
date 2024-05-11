# TODO: Change it to use shared task with celery and redis
# @shared_task(bind=True, max_retries=2, queue='check_tasks')
# def check_tasks(self):
#     pending_tasks = models.Transaction.objects.filter(ended_at__isnull=True).all()
#     for task in pending_tasks:
#         async_result = AsyncResult(str(task.task_id))
#         if async_result:
#             if async_result.state in [states.SUCCESS, states.REVOKED, states.FAILURE]:
#                 task.ended_at = now()
#                 task.task_status = async_result.state
#                 task.save()

# TODO: Change it to use periodic task with celery and redis, don't forget of create it on celery.py
# @app.task(bind=True, max_retries=1, queue='default')
# def your_periodic_task(self):
#     try:
#         # do stuff
#     except Exception as ex:
#         self.retry(exc=ex, countdown=2 ** self.request.retries)
