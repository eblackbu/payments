from django.db import connection

from paymentAPI.celery import app


@app.task(ignore_result=True)
def update_accounts():
    with connection.cursor() as cursor:
        cursor.execute("begin")
        cursor.execute("lock table payment_paymentaccount in ACCESS EXCLUSIVE MODE")
        cursor.execute("update payment_paymentaccount set balance = balance - \"hold\"")
        cursor.execute("update payment_paymentaccount set \"hold\" = 0")
        cursor.execute("commit")
