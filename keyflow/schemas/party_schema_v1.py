from marshmallow import Schema, fields


class PartySchemaV1(Schema):
    id = fields.Int(attribute="id")
    title = fields.String(attribute="title")
    address = fields.String(attribute="address")
    startTime = fields.DateTime(attribute="start_time")
    endTime = fields.String(attribute="end_time")
    ownerGAId = fields.Int(attribute="owner_ga.id")
