from db import db

# 添加中间表，不需要创建模型
article_tag_table = db.Table(
    "article_tag_table",
    db.Column("article_ id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("tag_ id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
)
class Article(db.Model):
    # 创建表结构操作
    # 表名
    __tablename__ = 'article'
    #  字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 使用关系
    # backref：会自动给User模型添加一个articles的属性，来获取文章列表
    author = db.relationship("User", backref="articles")

    tags = db.relationship("Tag", secondary=article_tag_table, back_populates="articles")

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    articles = db.relationship("Article", secondary=article_tag_table, back_populates="articles")
