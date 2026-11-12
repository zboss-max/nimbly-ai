from app.extensions import db
from app.models.base_model import BaseModel


class KnowledgeEntry(BaseModel, db.Model):
    """正式知识条目"""

    __tablename__ = 'knowledge_entry'

    id = db.Column(db.Integer, primary_key=True)

    # 知识属于哪个用户
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
        index=True,
    )

    # 基本内容
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # user：用户手动记录；ai：以后由智能体记录
    source = db.Column(
        db.String(16),
        nullable=False,
        default='user',
    )

    # active：正常；archived：归档；trash：回收站
    status = db.Column(
        db.String(16),
        nullable=False,
        default='active',
        index=True,
    )

    # 是否允许以后的智能体读取
    agent_enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    is_pinned = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    # 后续提醒和有效期功能使用，现在允许为空
    expires_at = db.Column(db.DateTime, nullable=True)
    remind_at = db.Column(db.DateTime, nullable=True)

    # 软删除时间：有值表示进入回收站
    deleted_at = db.Column(db.DateTime, nullable=True)

    @staticmethod
    def _format_time(value):
        if value is None:
            return None
        return value.strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        """把模型转换成接口可以返回的字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'status': self.status,
            'agent_enabled': self.agent_enabled,
            'is_pinned': self.is_pinned,
            'expires_at': self._format_time(self.expires_at),
            'remind_at': self._format_time(self.remind_at),
            'deleted_at': self._format_time(self.deleted_at),
            'create_time': self._format_time(self.create_time),
            'update_time': self._format_time(self.update_time),
        }
