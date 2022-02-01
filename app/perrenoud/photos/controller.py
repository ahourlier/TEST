from flask import request, jsonify
from flask_accepts import accepts, responds
from app.common.api import AuthenticatedApi
from . import api
from app.perrenoud.photos.error_handlers import (
    MissingPhotoException,
    MissingSectionException,
    MissingRoomException,
)
from app.perrenoud.photos.schema import PhotoSchema, PhotoAddSchema, PhotoFetchSchema
from app.perrenoud.photos.service import PhotoService


@api.route("/<int:project_id>/upload")
@api.param("ProjectId", "Project unique ID")
class PhotoUploadResource(AuthenticatedApi):
    """Photos upload for front mobile"""

    @accepts(api=api)
    @responds(schema=PhotoSchema(many=True))
    def post(self, project_id):
        """Upload a photo"""
        if "photo" not in request.files:
            raise MissingPhotoException()
        if "section" not in request.form:
            raise MissingSectionException()
        photos = request.files.getlist("photo")
        section = request.form.get("section")
        if section == "room" and "room_id" not in request.form:
            raise MissingRoomException()
        room_id = request.form.get("room_id")
        accommodation_id = request.form.get("accommodation_id")
        scenario_id = request.form.get("scenario_id")
        return PhotoService.upload_multiple(
            project_id,
            accommodation_id,
            photos,
            section,
            room_id=room_id,
            scenario_id=scenario_id,
        )


@api.route("/<int:project_id>/add")
@api.param("projectId", "Project unique ID")
class ProjectDocumentResource(AuthenticatedApi):
    @accepts(schema=PhotoAddSchema, api=api)
    @responds(schema=PhotoSchema(many=True))
    def post(self, project_id: int):
        data = request.parsed_obj
        response = PhotoService.add_multiple_photos(
            project_id,
            data.get("photos"),
            data.get("section"),
            accommodation_id=data.get("accommodation_id"),
            room_id=data.get("room_id"),
            scenario_id=data.get("scenario_id"),
        )
        return jsonify(response)


@api.route("/")
class PhotoListResource(AuthenticatedApi):
    @accepts(schema=PhotoFetchSchema, api=api)
    @responds(schema=PhotoSchema(many=True))
    def put(self):

        return PhotoService.fetch_photos(request.parsed_obj)
