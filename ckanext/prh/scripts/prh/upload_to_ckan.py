from ckanapi import LocalCKAN, ValidationError

registry = LocalCKAN()


def upload_to_ckan(package_id, filename):

    try:
        registry.action.package_patch(id=package_id, upload=open(filename, 'rb'))
    except ValidationError as e:
        print("Resource patch failed: %s")

