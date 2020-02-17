from datetime import datetime

from ckan.lib import mailer
import ckan.plugins.toolkit as t

from ckanapi import LocalCKAN, ValidationError

registry = LocalCKAN()


def upload_to_ckan(package_id, filename):

    try:
        resource = registry.action.resource_create(package_id=package_id, upload=open(filename, 'rb'))

        email_notification_recipients = t.aslist(t.config.get('ckanext.prh_tools.mail_recipients', ''))
        site_title = t.config.get('ckan.site_title', '')
        today = datetime.now().date().isoformat()

        msg = '%(site_title)s - PRH data uploaded %(today)s\n\n%(status)s' % {
            'site_title': site_title,
            'today': today,
            'status': "New data available in https://www.avoindata.fi/data/dataset/%s/resource/%s"
                      % (package_id, resource.get('id'))
        }

        for recipient in email_notification_recipients:
            email = {'recipient_name': '',
                     'recipient_email': recipient,
                     'subject': '%s - PRH data uploaded %s' % (site_title, today),
                     'body': msg}

            try:
                mailer.mail_recipient(**email)
            except mailer.MailerException as e:
                print 'Sending prh data notification to %s failed: %s' % (recipient, e)

    except ValidationError as e:
        print("Resource patch failed: %s" % e.error_summary)
