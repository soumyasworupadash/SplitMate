from sqlalchemy.orm import Session

from app.models.activity_log import Activity


def log_activity(
    group_id: int,
    user_id: int,
    action: str,
    description: str,
    db: Session
):
    activity = Activity(
        group_id=group_id,
        user_id=user_id,
        action=action,
        description=description
    )

    db.add(activity)
    db.commit()



def get_group_activity(
    group_id: int,
    db: Session
):
    return (
        db.query(Activity)
        .filter(Activity.group_id == group_id)
        .order_by(Activity.created_at.desc())
        .all()
    )


from app.models.group_member import GroupMember


def get_my_activity(
    current_user,
    db: Session
):
    memberships = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id)
        .all()
    )

    group_ids = [m.group_id for m in memberships]

    return (
        db.query(Activity)
        .filter(Activity.group_id.in_(group_ids))
        .order_by(Activity.created_at.desc())
        .limit(10)
        .all()
    )