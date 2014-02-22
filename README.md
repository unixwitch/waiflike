Waiflike is a simple content management system based on
[Wagtail](https://github.com/torchbox/wagtail), the Django CMS from
[Torchbox](http://www.torchbox.com/).  Waiflike takes Wagtail's easy-to-use
backend content management interface, and extends it with a functional theme
(based on Bootstrap) and Markdown text editing.  The result is a lightweight
but flexible complete CMS.  (Or, at least, it will be; Waiflike is still in the
very early stages and there are some rough edges.)

Waiflike is designed for creating simple, mostly static sites.  While you could
extend it to support more complicated features, you may be better off using
Wagtail directly for that.

### Markdown syntax

Waiflike adds some useful extensions to the standard Markdown syntax:

* Link to a page: `<:The page name>` or `<:The page name|link title>`
* After uploading an image, to display it in a page: `<:image:The image name>`
* Specify the image width in pixels: `<:image:The image name|width=150>`
* Align an image: `<:image:The image name|width=500|right>` (valid alignments are `left`, `right`, and `fullwidth`)
* Syntax highlighting:

<pre>
    #!c
    int main() {
        printf("hello, world\n");
        return 0;
    }
</pre>

### Installation

NB: Sadly, installation is more complicated than it should be for a lightweight
CMS right now (especially since Wagtail requires node.js).  Suggestions (or
pull requests!) to simplify installation would be appreciated.

#### Install Waiflike

* [Install node.js](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager)
* Install NPM: `curl https://npmjs.org/install.sh | sh`
* Install `less` and `coffeescript`:  `npm install -g less coffee-script`
* Install virtualenv, virtualenvwrapper and pip
* Create a new user to run Waiflike as.  This is not required, but strongly
  recommended.
* As the `waiflike` user:

<pre>
# Fetch Waiflike from git:
$ git clone https://github.com/ftarnell/waiflike.git

# Install dependencies
$ cd waiflike
$ mkvirtualenv waiflike
$ workon waiflike
$ pip install -r etc/requirements.txt

# Set up the database
$ ./manage.py syncdb
$ ./manage.py migrate

# Create static files:
$ ./manage.py collectstatic
</pre>

* Copy `waiflikeapp/settings/local.py_example` to `waiflikeapp/settings/local.py`
  and edit it as needed.  You will want to configure the database settings at least.
* You should now be able to run `./manage.py runserver`, visit http://localhost:8080,
  and see "Welcome to your new Wagtail site!".

Next, you'll want to run it under a web server.

#### Set up for nginx

* Install supervisord
* Copy `etc/supervisor.conf` to `/etc/supervisor/conf.d/waiflike.conf`
* `supervisorctl update`
* Create `/etc/nginx/conf.d/waiflike.conf`:

<pre>
server {
	listen   80;
	listen   [::]:80 ipv6only=on;

	server_name waiflike.local;

	location /static/ {
		alias /home/vagrant/waiflike/static/;
	}

	location / {
		include uwsgi_params;
		uwsgi_pass unix:/home/waiflike/waiflike/waiflike.sock;
		break;
	}
}
</pre>

* `nginx -s reload`

**Note**: Currently, Waiflike cannot be run in a subdirectory of the website; it
must be installed in the root.  This is due to [a Wagtail bug](https://github.com/torchbox/wagtail/issues/69).

#### Add initial content

* Visit http://<url>/admin, and log in with the superuser account you created
  earlier.
* Select the welcome page from the sidebar and delete it.
* Create a new page; when prompted for a type, select 'Site Page'.  This will be
  your main page.
* Visit http://<url>/django-admin.  Create a new Site, and select the page you
  just created as the default page.
