from celery import shared_task

from flow.models import Job
from flow.nodes.base import NodeContext


@shared_task()
def add(a, b):
    return a + b


@shared_task()
def run_flow(flow_id: int, input_context: NodeContext) -> NodeContext:
    from flow.executor import Executor
    from flow.models import Flow
    flow = Flow.objects.get(id=flow_id)
    # create job by flow
    job = Job.objects.create(flow=flow,
                             name=flow.name,
                             description=flow.description,
                             input=input_context)

    executor = Executor(flow)
    result = executor.execute(input_context)
    job.output = result
    job.save()
    return result
