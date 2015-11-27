---
layout: post
title:  Alembic migrate postgres sequence
description: Rename posgres sequences when renaming tables
date:   2015-11-27 09:56:00
categories: Python
---
I'm a fan of using SQLAlchemy and Posgres, I like to use it with Alembic to managed database migrations. My normal workflow with Alembic is:

1. Edit SQLAlchemy models
2. Autogenerate the migration{% highlight bash %}
alembic -c alembic.ini revision --autogenerate -m "Migration description"{% endhighlight %}
3. Run the migration{% highlight bash %}alembic -c alembic.ini upgrade head{% endhighlight %}

Now let's say there's a scenario where I have business critical software which tracks when I buy and eat Marathon bars. Now Marathon bars were renamed to Snickers in 1990 in the UK so it makes sense to update my sofware to reflect this and avoid confusion with legacy chocolate bar naming.


I have a SQLAlchemy model called `Marathon` which represents a DB table `marathon`. I want to rename the model to `Snickers` and have my DB table called `snickers`. The original `Marathon` model look like this:

{% highlight python %}
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Marathon(Base):
    __tablename__ = 'marathon'
    id = Column(Integer, primary_key=True)
    weight = Column(Integer, nullable=False)
    bought = Column(DateTime(timezone=True), nullable=False)
    eaten = Column(DateTime(timezone=True), nullable=False)
{% endhighlight %}

I edit it to look like this:


{% highlight python %}
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Snickers(Base):
    __tablename__ = 'snickers'
    id = Column(Integer, primary_key=True)
    weight = Column(Integer, nullable=False)
    bought = Column(DateTime(timezone=True), nullable=False)
    eaten = Column(DateTime(timezone=True), nullable=False)
{% endhighlight %}

I then run:

{% highlight bash %}
alembic -c alembic.ini revision --autogenerate -m "Renaming Marathon model to Snickers"
{% endhighlight %}

This produces the following migration for upgrade:

{% highlight python %}
def upgrade():
    op.create_table('snickers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('bought', sa.DateTime(timezone=True), nullable=False),
    sa.Column('eaten', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('marathon')
{% endhighlight %}

The issue with the migration is it's dropping the marathon table and creating a new snickers table. This is going to be a problem if I want to keep existing data, as it'll be deleted along with the marathon table. I need to manually edit the migration to use the alembic rename table command:

{% highlight python %}
def upgrade():
    op.rename_table('marathon', 'snickers')
{% endhighlight %}

All seams good in the world until I take a look in postgres. Running `\d` shows:

{% highlight bash %}
snacks=# \d
              List of relations
 Schema |      Name       |   Type   | Owner
--------+-----------------+----------+--------
 public | alembic_version | table    | snacks
 public | marathon_id_seq | sequence | snacks
 public | snickers        | table    | snacks
(3 rows)
{% endhighlight %}

What is `marathon_id_seq` doing hanging about? On further inspection of the snickers table `\d snickers` I can see that it's used for autoincrementing the id on the snickers table id field:
{% highlight bash %}
snacks=# \d snickers
                                  Table "public.snickers"
 Column |           Type           |                       Modifiers
--------+--------------------------+-------------------------------------------------------
 id     | integer                  | not null default nextval('marathon_id_seq'::regclass)
 weight | integer                  | not null
 bought | timestamp with time zone | not null
 eaten  | timestamp with time zone | not null
Indexes:
    "marathon_pkey" PRIMARY KEY, btree (id)
{% endhighlight %}


on my database show's there's still a sequence called `xxxx___marathon__xxxx`, running `\d marathon` show that this
# show autoincrementing sequence is incorrect


#TODO: talk about indexes (would migration work without them)
# add extra code for the sequence code

# Conclusion I'm not aware if this is available in Alembic but contact me if it is. A interest project would be to edit Alembic to automatically detect table renames. Might need a custom command, to realise it's not a drop and create. Detect like git does (check it doesn't have one already).

# TODO: add versions
