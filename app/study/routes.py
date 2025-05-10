from flask import request
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app import mongo
from app.study.forms import CreateGroupForm
from app.study import study
from bson.objectid import ObjectId  
from werkzeug.utils import secure_filename
import os
from app.study.forms import CommentForm


UPLOAD_FOLDER = 'app/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@study.route('/create-group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm() 
    
    if form.validate_on_submit(): 
        tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        
        group_data = {
            "course_name": form.course_name.data.strip(),
            "description": form.description.data.strip(),
            "tags": tags,
            "created_by": current_user.username,  
            "created_at": datetime.utcnow(),
            "members": [current_user.username]    
        }
        
        try:
            mongo.db.groups.insert_one(group_data)
            flash('Study group created successfully!', 'success')
            
            return redirect(url_for('study.my_groups'))
        
        except Exception as e:
            current_app.logger.error(f"Group creation error: {e}")
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('study/create_group.html', form=form)

@study.route('/my-groups')
@login_required
def my_groups():
    try:
        user_groups = list(mongo.db.groups.find({"created_by": current_user.username}))
    except Exception as e:
        current_app.logger.error(f"Error fetching groups: {e}")
        user_groups = []

    return render_template('study/my_groups.html', groups=user_groups)


@study.route('/group/<group_id>', methods=['GET', 'POST'])
@login_required
def view_group(group_id):
    from app.study.forms import ScheduleSessionForm, ResourceForm, CommentForm
    form = ScheduleSessionForm()
    resource_form = ResourceForm()
    comment_form = CommentForm()

    try:
        group = mongo.db.groups.find_one({"_id": ObjectId(group_id)})
        if not group:
            flash("Study group not found.", "danger")
            return redirect(url_for('study.my_groups'))

        if form.validate_on_submit() and form.submit.data:
            session_data = {
                "group_id": ObjectId(group_id),
                "created_by": current_user.username,
                "date_time": form.date_time.data,
                "zoom_link": form.zoom_link.data.strip() if form.zoom_link.data else None,
                "created_at": datetime.utcnow()
            }
            mongo.db.sessions.insert_one(session_data)
            flash("Session scheduled successfully!", "success")
            return redirect(url_for('study.view_group', group_id=group_id))

        filename = None
        file_path = None
        if resource_form.validate_on_submit() and resource_form.submit.data:
            if resource_form.file.data:
                filename = secure_filename(resource_form.file.data.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                resource_form.file.data.save(file_path)

            resource_data = {
                "group_id": ObjectId(group_id),
                "uploaded_by": current_user.username,
                "title": resource_form.title.data,
                "description": resource_form.description.data,
                "file_url": f"/static/uploads/{filename}" if filename else None,
                "link": resource_form.link.data.strip() if resource_form.link.data else None,
                "uploaded_at": datetime.utcnow()
            }
            mongo.db.resources.insert_one(resource_data)
            flash("Resource shared successfully!", "success")
            return redirect(url_for('study.view_group', group_id=group_id))

        if comment_form.validate_on_submit() and comment_form.submit.data:
            comment_data = {
                "group_id": ObjectId(group_id),
                "author": current_user.username,
                "content": comment_form.content.data.strip(),
                "posted_at": datetime.utcnow()
            }
            mongo.db.comments.insert_one(comment_data)
            flash("Comment posted!", "success")
            return redirect(url_for('study.view_group', group_id=group_id))
        sessions = list(mongo.db.sessions.find({"group_id": ObjectId(group_id)}).sort("date_time", 1))
        resources = list(mongo.db.resources.find({"group_id": ObjectId(group_id)}).sort("uploaded_at", -1))
        comments = list(mongo.db.comments.find({"group_id": ObjectId(group_id)}).sort("posted_at", -1))

    except Exception as e:
        current_app.logger.error(f"Error loading group: {e}")
        flash("An unexpected error occurred.", "danger")
        return redirect(url_for('study.my_groups'))

    return render_template(
        'study/view_group.html',
        group=group,
        form=form,
        resource_form=resource_form,
        comment_form=comment_form,
        sessions=sessions,
        resources=resources,
        comments=comments
    )

@study.route('/join', methods=['GET', 'POST'])
@login_required
def join_groups():
    try:
        all_groups = list(mongo.db.groups.find({}))

        if request.method == 'POST':
            group_id = request.form.get('group_id')
            group = mongo.db.groups.find_one({"_id": ObjectId(group_id)})

            if not group:
                flash("Group not found.", "danger")
                return redirect(url_for('study.join_groups'))

            if current_user.username not in group.get('members', []):
                mongo.db.groups.update_one(
                    {"_id": ObjectId(group_id)},
                    {"$push": {"members": current_user.username}}
                )
                flash(f"You joined {group['course_name']}!", "success")
            else:
                flash("You are already a member of this group.", "info")

            return redirect(url_for('study.join_groups'))

        return render_template('study/join_groups.html', groups=all_groups)

    except Exception as e:
        current_app.logger.error(f"Error in join_groups: {e}")
        flash("Something went wrong.", "danger")
        return redirect(url_for('study.my_groups'))


