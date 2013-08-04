import cgi

import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import mail

import datetime

class Reminder(db.Model):
    author = db.UserProperty()
    message = db.StringProperty(multiline=True)
    datetime = db.DateTimeProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            reminders_query = db.GqlQuery("SELECT * FROM Reminder WHERE author = :1 ORDER BY datetime DESC",user)
            reminders = reminders_query.fetch(1000)
            template_values = {
            'reminders': reminders,
            'user': user,
            'url': url
            }
            path = os.path.join(os.path.dirname(__file__), 'logged_in.html')
            self.response.out.write(template.render(path, template_values))
        else:
            url = users.create_login_url(self.request.uri)
            template_values = {'url': url}
            path = os.path.join(os.path.dirname(__file__), 'logged_out.html')
            self.response.out.write(template.render(path, template_values))

class RemindersAdd(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            reminder = Reminder()
            reminder.author = user
            reminder.message = self.request.get('message')
            days = int(self.request.get('days'))
            reminder.datetime = datetime.datetime.now() + datetime.timedelta(days=days)
            reminder.put()
        self.redirect('/')

class RemindersDelete(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        key = self.request.get('key')
        if user:
            reminder = Reminder.get(key)
            if reminder and (reminder.author == user):
                reminder.delete()
        self.redirect('/')

class RemindersProcess(webapp.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        reminders = Reminder.all().run()
        for reminder in reminders:
            if reminder.datetime <= now:
                message = mail.EmailMessage(sender="Email Reminder <reminder@solvinggames.appspotmail.com>",
                                            subject="Your reminder")
                message.to = reminder.author.email()
                message.body = reminder.message
                message.send()
                reminder.delete()

class InboundEmailProcess(webapp.RequestHandler):
    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        # do something with the message
            

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/add', RemindersAdd),
                                     ('/delete', RemindersDelete),
                                     ('/process', RemindersProcess),
                                     ('/_ah/mail/.+', InboundEmailProcess)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
