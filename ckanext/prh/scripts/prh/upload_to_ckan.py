from ckanapi import LocalCKAN, ValidationError

registry = LocalCKAN()


def upload_to_ckan(package_id, filename):

    try:
        registry.action.resource_create(package_id=package_id, upload=open(filename, 'rb'))
    except ValidationError as e:
        print("Resource patch failed: %s" % e.error_summary)
