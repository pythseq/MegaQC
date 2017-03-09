# MultiQC_DB Installation: Production

### NB: Placeholder text. Package is not yet ready for production use.

### 2) Install MultiQC_DB package
MultiQC_DB is available on both the Python Package Index (PyPI) and
conda (bioconda channel). To install using PyPI do the following command:

```bash
pip install multiqc_db
```

To install with conda:

```bash
conda install -c bioconda multiqc_db
```

### 1) Set up database
> MultiQC_DB uses the Flask SQLAlchemy plugin, meaning that it can be used
> with any SQL database (_PostgreSQL_, _MySQL_, _SQLite_ and others).
>
> If you have a preference for any of the above, feel free to use that.
> The instructions below describe how to set up a PostgreSQL database.

First, install PostgreSQL. On a linux machine, this can be done with `apt-get`:

```bash
sudo apt-get install postgresql postgresql-contrib
```

If you're on a mac, you can do this with homebrew:

```bash
brew install postgresql
```

For other systems, see the [PostgreSQL documentation](https://www.postgresql.org/download/).

Next, create a PostgreSQL database:

```bash
cd /path/to/database/multiqc_db
initdb -D postgres/data/
```

MultiQC_DB uses environment variables to store sensitive data, such as
database passwords. Add the following lines to your `~/.bashrc` file so
that the variables are set up every time a shell is loaded:

```bash
export MULTIQC_DB_DBNAME='[ DATABASE NAME HERE ]'
export MULTIQC_DB_DBUSER='[ RANDOM USERNAME ]'
export MULTIQC_DB_DBPASSWORD='[ REALLY SECURE PASSWORD ]'
export MULTIQC_DB_DBPATH="postgresql://$MULTIQC_DB_DBUSER:$MULTIQC_DB_DBPASSWORD@localhost/$MULTIQC_DB_DBNAME"
export MULTIQC_DB_POSTGRES='/path/to/database/multiqc_db/postgres/'
```

Now we can create a new database for the website to use:

```bash
echo $MULTIQC_DB_DBPASSWORD # so you can copy it for the prompt in a second!
createuser -s $MULTIQC_DB_DBUSER --pwprompt --createdb --no-superuser --no-createrole
# paste password in prompt
createdb -U $EELSDB_DB_USER --locale=en_US.utf-8 -E utf-8 -O $EELSDB_DB_USER $EELSDB_DB_NAME -T template0
```

### 3) Configure MultiQC_DB
Now that everything is installed, we need to add a few more environment
variables to configure the Flask server behind MultiQC_DB.

Add the following lines to your `~/.bashrc` file so that the variables are
set every time a shell is loaded:

```bash
export MULTIQC_DB_SECRET='[ SOMETHING REALLY SECRET ]'
export FLASK_APP=multiqc_db.app
export FLASK_DEBUG=false

export MULTIQC_DB_DBNAME='[ DATABASE NAME HERE ]'
export MULTIQC_DB_DBUSER='[ RANDOM USERNAME ]'
export MULTIQC_DB_DBPASSWORD='[ REALLY SECURE PASSWORD ]'
export MULTIQC_DB_DBPATH="postgresql://$MULTIQC_DB_DBUSER:$MULTIQC_DB_DBPASSWORD@localhost/$MULTIQC_DB_DBNAME"
export MULTIQC_DB_POSTGRES='/path/to/database/multiqc_db/postgres/'
```

Finally, initialise and update the MultiQC_DB database:

```bash
flask db init
flask db migrate
flask db upgrade
```

### 4) Running MultiQC_DB
Once everything is installed and configured, you can run the `flask` server
application to launch the MultiQC_DB website. 

```bash
flask run
```

This should give some log messages, including the address where the website
can be viewed in the browser.

> NB: The Flask server application above is designed for development work.
> While lightweight and easy to use it is not suitable for production
> for a site with a lot of traffic, as it doesn’t scale well and by default
> serves only one request at a time.
>
> It will probably be fine as long as the site is very low traffic, but
> anything more than that and you will want to look into the
> [Flask Deployment Options](http://flask.pocoo.org/docs/0.12/deploying/)
> documentation which has lots of options. For example,
> [mod_wsgi (Apache)](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/).

