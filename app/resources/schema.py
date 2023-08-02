import marshmallow as ma

class TaskSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("task_id", "task", "complete")
