r"""
`TestExecution` use RQ queue ID an UUID as primary key::

    >>> from uuid import uuid4
    >>> rq_jid = uuid4()
    >>> te = TestExecution.objects.create(
    ...     pk=rq_jid,
    ...     origin=default_test_data,
    ...     )
    >>> assert te.pk == te.rq_jid

(conti.) Don't insert bytes string into `output` char field::

    >>> pb = ConsoleLine.objects.create(test_execution=te, output='')

    >>> pb.output = b'3 critical tests, 3 passed, 0 failed'
    >>> pb.output
    b'3 critical tests, 3 passed, 0 failed'
    >>> pb.save() ; pb.refresh_from_db()
    >>> pb.output
    "b'3 critical tests, 3 passed, 0 failed'"

    >>> pb.output = b'3 critical tests, 3 passed, 0 failed'.decode()
    >>> pb.output
    '3 critical tests, 3 passed, 0 failed'
    >>> pb.save() ; pb.refresh_from_db()
    >>> pb.output
    '3 critical tests, 3 passed, 0 failed'
"""


from django.conf import settings
from django.db import models


default_test_data = __import__('json').dumps({
    'filename': 'basic.robot',
    'content': '*** test cases ***\nTC\n  log  message  console=yes\n',
    })


class TestData(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_data = models.TextField(default=default_test_data)  # TODO: validator
    last_modified = models.DateTimeField(auto_now=True)
    #refer_to = models.CharField(...)


class TestExecution(models.Model):
    rq_jid = models.UUIDField(primary_key=True)
    start = models.DateTimeField(auto_now_add=True)
    test_data = models.ForeignKey(TestData, on_delete=models.CASCADE, null=True)
    origin = models.TextField(null=True)
    pid = models.PositiveSmallIntegerField(null=True)

    def submit(*a, **kw): ...
    def stop(*a, **kw): ...
    def get_console(*a, **kw): ...


class ConsoleLine(models.Model):
    test_execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE)
    output = models.CharField(max_length=256, default=None)


class TestResult(models.Model):
    test_execution = models.OneToOneField(TestExecution, on_delete=models.CASCADE, related_name='test_result')
    console = models.TextField()
    report = models.TextField()
    log = models.TextField()
    output = models.TextField()