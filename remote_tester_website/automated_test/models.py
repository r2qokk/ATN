import json
import uuid

from django.db import models
from django.conf import settings


DEFAULT_TEST_DATA = json.dumps({
    'filename': 'basic.robot',
    'content': '*** test cases ***\nTC\n  log  message  console=yes\n',
    })


class ExecLayer(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')


class Sut(models.Model):
    uuid = models.UUIDField(primary_key=True)
    exec_layer = models.ForeignKey(ExecLayer, on_delete=models.CASCADE)
    # TODO: improve OOBM
    type = models.CharField(max_length=64)
    credential = models.CharField(max_length=64)
    reserved_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            related_name='reserved_sut', null=True, blank=True,
            )
    maintained_by = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
            related_name='maintained_sut', null=True,
            )


class TestData(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_data = models.TextField(default=DEFAULT_TEST_DATA)
    last_modified = models.DateTimeField(auto_now=True)
    #refer_to = models.CharField(...)


class TestExecution(models.Model):
    rq_jid = models.UUIDField(null=True, blank=True)
    start = models.DateTimeField(auto_now_add=True)
    test_data = models.ForeignKey(TestData, on_delete=models.SET_NULL, null=True)
    origin = models.TextField(null=True)


class TestResult(models.Model):
    test_execution = models.OneToOneField(TestExecution, on_delete=models.CASCADE, related_name='test_result')
    console = models.TextField()
    report = models.TextField()
    log = models.TextField()
    output = models.TextField()
