from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Flow(TimeStampedModel):
    """
    Flow is a flow of nodes
    """
    STATUS_CHOICES = Choices(
        (0, 'draft', 'Draft'),
        (1, 'active', 'Active'),
        (2, 'active', 'Active'),
    )
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=500)
    status = models.IntegerField("Status", choices=STATUS_CHOICES, default=STATUS_CHOICES.draft)
    nodes = models.ManyToManyField("Node", blank=True)

    def __str__(self):
        return self.name


class Node(TimeStampedModel):
    """
    Node is a node in a flow. It can be a trigger node, an action node, or a logic node
    """
    TYPE = Choices(
        (0, 'trigger', 'Trigger'),
        (1, 'action', 'Action'),
        (2, 'logic', 'Logic'),
    )
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=500)
    node_type = models.IntegerField("Node Type", choices=TYPE)
    code = models.CharField("Code", max_length=100, unique=True)
    sub_nodes = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.name


class Option(TimeStampedModel):
    """
    Option is a expression option for other node properties
    """
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=500)
    code = models.CharField("Code", max_length=100)
    node = models.ForeignKey("Node", on_delete=models.CASCADE, related_name="options")
    option_type = models.ForeignKey("OptionType", on_delete=models.CASCADE, related_name="options")

    def __str__(self):
        return self.name


class OptionType(TimeStampedModel):
    """
    OptionType is a type of option
    """
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=500)
    accepts = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.name


class Job(TimeStampedModel):
    """
    Job is a run instance job of a flow
    """
    STATUS_CHOICES = Choices(
        (0, 'started', 'Started'),
        (1, 'processing', 'Processing'),
        (2, 'finished', 'Finished'),
    )
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=500)
    status = models.IntegerField("Status", choices=STATUS_CHOICES, default=STATUS_CHOICES.started)
    flow = models.ForeignKey("Flow", on_delete=models.CASCADE, related_name="jobs")
    input = models.JSONField("Input", blank=True, null=True)
    output = models.JSONField("Output", blank=True, null=True)

    def __str__(self):
        return self.name


class JobExecution(TimeStampedModel):
    """
    JobExecution is a run instance execution of a job
    """
    STATUS_CHOICES = Choices(
        (0, 'started', 'Started'),
        (1, 'processing', 'Processing'),
        (2, 'finished', 'Finished'),
    )
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=500)
    status = models.IntegerField("Status", choices=STATUS_CHOICES, default=STATUS_CHOICES.started)
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="executions")
    node = models.ForeignKey("Node", on_delete=models.CASCADE, related_name="executions")
    input = models.JSONField("Input", blank=True, null=True)
    output = models.JSONField("Output", blank=True, null=True)

    def __str__(self):
        return self.name
