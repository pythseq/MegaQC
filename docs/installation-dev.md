# MultiQC_DB Installation: Development

If doing development work with MultiQC_DB, we recommend following a
slightly different installation procedure. The instructions below will
set up a lightweight installation with example data and lots of debugging help.

It is not suitable for a production environment. If you want to run
MultiQC_DB for your group, see the [production installation](installation-dev.md)
instructions instead.

### 1) Grab the code
Pull the latest development code from GitHub (modify the URL if using
your own forked version) and install the required packages:

```bash
git clone https://github.com/ewels/MultiQC_DB
cd MultiQC_DB
python setup.py develop
pip install -r requirements/dev.txt
```

The installation may complain that `Error: pg_config executable not found.`
If so, you need to install PostgreSQL first. On a linux machine, this can be
done with `apt-get`:

```bash
sudo apt-get install postgresql postgresql-contrib
```

If you're on a mac, you can do this with homebrew:

```bash
brew install postgresql
```

For other systems, see the [PostgreSQL documentation](https://www.postgresql.org/download/).

#### JavaScript and CSS
The code on GitHub doesn't include any of the front-end packages, so
you need to fetch them using `bower`, itself installed using `npm`.
All of the front end CSS and JavaScript is combined and minified using
`Grunt` (also installed by `npm`).

The CSS in MultiQC_DB is written as sass (`*.scss` files). These need to
be compiled to `.css` files before they can be used by the web browser.
This is done automagically (see below), but needs the `sass` tool available
on the command line to do this. To install, run the following command:

```bash
gem install sass
```

> I recommend getting a copy of [`rbenv`](https://github.com/rbenv/rbenv) if you
> have any problems with Ruby.

Ok, nearly there. Now [install Node.js and `npm`](https://docs.npmjs.com/getting-started/installing-node).
Then, run the following commands in the MultiQC_DB directory:

```bash
npm install
bower install
grunt
```

This should install everything, fetch the front end files and compile them.

If you're working on the front-end javascript or SCSS, you'll want to run
`grunt watch` to automatically recompile every time you save changes.

### 2) Database setup
MultiQC_DB can work with any SQL database, but for development it's probably
simplest to use SQLite, which uses flat files and doesn't require any
background services.

If using SQLite, you don't need to do any setup, as the MultiQC_DB code
will create everything it needs.

### 3) MultiQC_DB configuration
Next, you need a few environment variables to tell Flask how to run the
server. Add the following to `.bashrc` or `.bash_profile`:

```bash
export MULTIQC_DB_SECRET='[ SOMETHING REALLY SECRET ]'
export FLASK_APP=multiqc_db.app
export FLASK_DEBUG=true
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


## Shell
To open the interactive shell, run:

```bash
flask shell
```

By default, you will have access to the flask `app`.


## Running Tests
To run all tests, run:

```bash
flask test
```

Note that the main GitHub repository will run tests using Travis every time
a commit or Pull Request is submitted. Travis can also be enabled on forked
repositories and should work automatically with the bundled `.travis.yml` file.

## Migrations
Whenever a database migration needs to be made. Run the following commands:

```bash
flask db migrate
```

This will generate a new migration script. Then run:

```bash
flask db upgrade
```

To apply the migration.

For a full migration command reference, run `flask db --help`.