---
layout: post
title:  Rename Postgres table with Alembic migrations
description: Rename PostgreSQL tables, sequences and indexes
date:   2015-11-27 09:56:00
categories: Python
---
In this article I'll discuss the approach I take to rename Postgres tables using Alembic. This includes renaming all references to the old table name such as sequences and indexes.

I'm a fan of SQLAlchemy and Postgres, I like to use them with Alembic to manage my database migrations. My normal workflow with Alembic is:

1. Edit SQLAlchemy models
2. Auto-generate the migration{% highlight bash %}
alembic -c alembic.ini revision --autogenerate -m "Migration description"{% endhighlight %}
3. Run the migration{% highlight bash %}alembic -c alembic.ini upgrade head{% endhighlight %}

Let's say I have business-critical software which tracks when I buy and eat Marathon bars. Marathon bars were renamed to Snickers in 1990 in the UK so it makes sense to update my software to reflect this, this will help avoid confusion with legacy chocolate bar naming.

I have an SQLAlchemy model called `Marathon` which represents a DB table `marathon`. I want to rename the model to `Snickers` and have my DB table called `snickers`. The original `Marathon` model looks like this:

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

The migration is dropping the `marathon` table and creating a new `snickers` table. This is going to be a problem if I want to keep existing data, as it'll be deleted along with the `marathon` table. I need to manually edit the migration to use the alembic `rename_table` command:

{% highlight python %}
def upgrade():
    op.rename_table('marathon', 'snickers')
{% endhighlight %}

All seems good in the world until I take a look in Postgres. Running `\d` shows:

{% highlight sql %}
snacks=# \d
              List of relations
 Schema |      Name       |   Type   | Owner
--------+-----------------+----------+--------
 public | alembic_version | table    | snacks
 public | marathon_id_seq | sequence | snacks
 public | snickers        | table    | snacks
(3 rows)
{% endhighlight %}

What is the troublesome `marathon_id_seq` doing hanging about?

On further inspection of the snickers table `\d snickers` I can see that `marathon_id_seq` is used for auto-incrementing the id:
{% highlight sql %}
snacks=# \d snickers
                                  Table "public.snickers"
 Column |  Type   | Modifiers
--------+---------+------------------------------------------------------
 id     | integer | not null default nextval('snickers_id_seq'::regclass)
{% endhighlight %}

I rename the sequence in the migration like this:

{% highlight python %}
op.execute('ALTER SEQUENCE  marathon_id_seq RENAME TO snickers_id_seq')
{% endhighlight %}

Are we finished? Of course not, this is a development blog post, we need at least three things to go wrong. Let's inspect the `snickers` table again to see our last problem:

{% highlight sql %}
snacks=# \d snickers
...
Indexes:
    "marathon_pkey" PRIMARY KEY, btree (id)
{% endhighlight %}

I've got this pesky index `marathon_pkey` hanging about. I can rename the index in the migration too:

{% highlight python %}
op.execute('ALTER INDEX marathon_pkey RENAME TO snickers_pkey')
{% endhighlight %}

This is my finished migration:

{% highlight python %}
def upgrade():
    op.rename_table('marathon', 'snickers')
    op.execute('ALTER SEQUENCE marathon_id_seq RENAME TO snickers_id_seq')
    op.execute('ALTER INDEX marathon_pkey RENAME TO snickers_pkey')

def downgrade():
    op.rename_table('snickers', 'marathon')
    op.execute('ALTER SEQUENCE snickers_id_seq RENAME TO marathon_id_seq')
    op.execute('ALTER INDEX snickers_pkey RENAME TO marathon_pkey')
{% endhighlight %}

Remember kids, winners don't do drugs and they always write downgrade database migrations.

It would be amazing if Alembic could automatically produce these type of rename migrations but I'm not sure if this is possible to implement. One solution would be to add an extra command to Alembic especially for renaming tables. The code for my example project is over on [Github](https://github.com/pxg/alembic_rename).
