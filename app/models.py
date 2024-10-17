from sqlalchemy import Column, Integer, Boolean, Numeric, String, ForeignKey, Text, Index, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from . database import Base


# CREATING ORM MODEL FOR [posts] TABLE
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    # Adding relationship (Foreign key relationship)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    # Retrieving using relationship
    # Then in schema (schema.py), we indicated the relation query to return is joints so in Post class we return
    # owner owner: UserOut. UserOut is the reponse model, responding to this joint
    # The "User" here means the users table on this ORM model basically returning the model class User
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)


# I JUST ADDED THIS TO EXPLORE SOME UNUSED TERMS
class PostCategory(Base):
    __tablename__ = "post_categories"
    catagory_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(400), nullable=False)
    category_content = Column(Text, nullable=True)
    category_price = Column(Numeric(10, 2), nullable=False)
    contact_email = Column(String(500), nullable=False)
    category_state = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    # Ceating index and defning constraints
    # You can only do index. or do only constraints or do both
    # In my example i did both just to try it out
    __table_args__ = (
        # Index
        Index('category_name_idx', 'category_name'),
        Index('category_price_idx', 'category_price'),
        Index('category_state_idx', 'category_state'),
        Index('category_email_idx', 'contact_email'),
        Index('created_at_idx', 'created_at'),

        # constraint
        UniqueConstraint('contact_email', name='contact_email_uq'),
        UniqueConstraint('category_state', name='category_state_uq'),

        # Adding Check constraint
        CheckConstraint('category_price > 0', name='check_price_ck')
    )
