import logging

from django.contrib import admin

from flow.models import Flow, Node, Option, Job, JobExecution

from django_object_actions import DjangoObjectActions, action

from flow.nodes.base import NodeContext

logger = logging.getLogger(__name__)


class FlowAdmin(DjangoObjectActions, admin.ModelAdmin):
    fields = ('name', 'description', 'status', 'nodes')
    list_display = ('name', 'description', 'status', 'created', 'modified')
    readonly_fields = ('status',)

    @action(
        label="Publish",  # optional
        description="Publish this flow"  # optional
    )
    def publish(self, request, obj):
        obj.status = Flow.STATUS_CHOICES.active
        obj.save()

    @action(
        label="DEBUG",  # optional
        description="DEBUG"  # optional
    )
    def debug(self, request, obj):
        logger.info("DEBUG")
        from flow.tasks import run_flow
        async_task = run_flow.delay(obj.id, NodeContext())
        result = async_task.get()
        logger.info("DEBUG result: %s", result)

    change_actions = ('publish', 'debug',)


class NodeAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'node_type', 'code', 'params', 'sub_nodes')
    list_display = ('name', 'description', 'node_type', 'code', 'params', 'created', 'modified')


class OptionAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'code', 'node', 'option_type', 'is_list')
    list_display = ('name', 'description', 'code', 'node', 'option_type', 'is_list', 'created', 'modified')


class JobAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'status', 'flow', 'input', 'output')
    list_display = ('name', 'description', 'status', 'flow', 'input', 'output', 'created', 'modified')


class JobExecutionAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'status', 'job', 'node', 'input', 'output')
    list_display = ('name', 'description', 'status', 'job', 'node', 'input', 'output', 'created', 'modified')


admin.site.register(Flow, FlowAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobExecution, JobExecutionAdmin)
