from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(allow_none=True)
    category = fields.Str(required=True)
    priority = fields.Str(required=True, validate=validate.OneOf(['Low', 'Medium', 'High']))
    deadline = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)