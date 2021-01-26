from marshmallow import Schema, fields


class PartyChatSchemaV1(Schema):
    id = fields.Int(attribute="id", required=False)
    message = fields.String(attribute="message", required=True, default="")
    parentMessageId = fields.Int(
        attribute="parent_chat_message", required=False, default=None
    )
