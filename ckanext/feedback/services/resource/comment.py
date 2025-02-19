from datetime import datetime

from ckan.model.resource import Resource
from flask import request

from ckanext.feedback.models.resource_comment import (
    ResourceComment,
    ResourceCommentCategory,
    ResourceCommentReply,
)
from ckanext.feedback.models.session import session


# Get resource from the selected resource_id
def get_resource(resource_id):
    return (
        session.query(
            Resource,
        )
        .filter(Resource.id == resource_id)
        .first()
    )


# Get comments related to the dataset or resource
def get_resource_comments(resource_id=None, approval=None):
    query = session.query(ResourceComment).order_by(ResourceComment.created.desc())
    if resource_id is not None:
        query = query.filter(ResourceComment.resource_id == resource_id)
    if approval is not None:
        query = query.filter(ResourceComment.approval == approval)

    return query.all()


# Get category enum names and values
def get_resource_comment_categories():
    return ResourceCommentCategory


# Create new comment
def create_resource_comment(resource_id, category, content, rating):
    comment = ResourceComment(
        resource_id=resource_id,
        category=category,
        content=content,
        rating=rating,
    )
    session.add(comment)


# Approve selected resource comment
def approve_resource_comment(resource_comment_id, approval_user_id):
    comment = session.query(ResourceComment).get(resource_comment_id)
    comment.approval = True
    comment.approved = datetime.now()
    comment.approval_user_id = approval_user_id


# Get reply for target comment
def get_comment_reply(resource_comment_id):
    return (
        session.query(ResourceCommentReply)
        .filter(ResourceCommentReply.resource_comment_id == resource_comment_id)
        .first()
    )


# Create new reply
def create_reply(resource_comment_id, content, creator_user_id):
    reply = ResourceCommentReply(
        resource_comment_id=resource_comment_id,
        content=content,
        creator_user_id=creator_user_id,
    )
    session.add(reply)


# Get cookie
def get_cookie(resource_id):
    return request.cookies.get(resource_id)
