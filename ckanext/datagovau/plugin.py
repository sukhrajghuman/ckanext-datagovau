import ckan.plugins as plugins
import ckan.lib as lib
import ckan.plugins.toolkit as tk
import ckan.model as model
import ckan.logic as logic
import ckanext.datastore.db as datastore_db
import os


import ckanext.datagovau.action as action
from ckan.lib.plugins import DefaultOrganizationForm
from ckan.lib import uploader, formatters

# get user created datasets and those they have edited
def get_user_datasets(user_dict):
    created_datasets_list = user_dict['datasets']
    active_datasets_list = [x['data']['package'] for x in
                            lib.helpers.get_action('user_activity_list', {'id': user_dict['id']}) if
                            x['data'].get('package')]
    raw_list = created_datasets_list + active_datasets_list
    filtered_dict = {}
    for dataset in raw_list:
        if dataset['id'] not in filtered_dict.keys():
            filtered_dict[dataset['id']] = dataset
    return filtered_dict.values()


def get_related_dataset(related_id):
    result = model.Session.execute(
        "select title from related_dataset inner join package on package.id = related_dataset.dataset_id where related_id =\'" + related_id + "\' limit 1;").first()[0]
    return result


def related_create(context, data_dict=None):
    return {'success': False, 'msg': 'No one is allowed to create related items'}


def get_ddg_site_statistics():
    stats = {}
    result = model.Session.execute("select count(*) from package where package.state='active' "
                                   "and package.type ='dataset' and package.private = 'f' ").first()[0]
    stats['dataset_count'] = result
    result = model.Session.execute("select count(*) from package where package.state='active' "
                                   "and package.type ='dataset' and package.private = 'f' and package.id in "
                                   "(select package_id from package_extra where key = 'unpublished' and value='True') ").first()[0]
    stats['unpub_data_count'] = result

    stats['open_count'] = logic.get_action('package_search')({}, {"fq":"isopen:true"})['count']

    result = model.Session.execute(
        '''select count(*) from related r
           left join related_dataset rd on r.id = rd.related_id
           where rd.status = 'active' or rd.id is null''').first()[0]
    stats['related_count'] = result
    result = model.Session.execute(
        '''select count(*) from resource
        where resource.state='active' and        
        (format='wms')
        and package_id not IN
        (select distinct package_id from package INNER JOIN package_extra
        on package.id = package_extra.package_id where key = 'harvest_portal')
        ''').first()[0]
    result = result + len(datastore_db.get_all_resources_ids_in_datastore())

    stats['api_count'] = result

    return stats

def get_resource_file_size(rsc):
    if rsc.get('url_type') == 'upload':
        upload = uploader.ResourceUpload(rsc)
        value = None
        try:
            value = os.path.getsize(upload.get_path(rsc['id']))
            value = formatters.localised_filesize(int(value))
        except Exception:
            # Sometimes values that can't be converted to ints can sneak
            # into the db. In this case, just leave them as they are.
            pass
        return value
    return None


class DataGovAuPlugin(plugins.SingletonPlugin,
                      tk.DefaultDatasetForm):
    '''An example IDatasetForm CKAN plugin.

    Uses a tag vocabulary to add a custom metadata field to datasets.

    '''
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IFacets, inherit=True)

    def dataset_facets(self, facets, package_type):
        if 'jurisdiction' in facets:
            facets['jurisdiction'] = 'Jurisdiction'
        if 'unpublished' in facets:
            facets['unpublished'] = 'Published Status'
        return facets

    def after_search(self, search_results, data_dict):
        if 'unpublished' in search_results['facets']:
            search_results['facets']['unpublished']['Published datasets'] = search_results['count'] - search_results['facets']['unpublished'].get('True',0)
            if 'True' in search_results['facets']['unpublished']:
                search_results['facets']['unpublished']['Unpublished datasets'] = search_results['facets']['unpublished']['True']
                del search_results['facets']['unpublished']['True']
            restructured_facet = {
                'title': 'unpublished',
                'items': []
                }
            for key_, value_ in search_results['facets']['unpublished'].items():
                new_facet_dict = {}
                new_facet_dict['name'] = key_
                new_facet_dict['display_name'] = key_
                new_facet_dict['count'] = value_
                restructured_facet['items'].append(new_facet_dict)
            search_results['search_facets']['unpublished'] = restructured_facet
        return search_results

    def get_auth_functions(self):
        return {'related_create': related_create}

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # here = os.path.dirname(__file__)
        # rootdir = os.path.dirname(os.path.dirname(here))

        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'theme/public')
        tk.add_resource('theme/public', 'ckanext-datagovau')
        tk.add_resource('public/scripts/vendor/jstree', 'jstree')
        # config['licenses_group_url'] = 'http://%(ckan.site_url)/licenses.json'

    def get_helpers(self):
        return {'get_user_datasets': get_user_datasets, 'get_related_dataset': get_related_dataset,
                'get_ddg_site_statistics': get_ddg_site_statistics, 'get_resource_file_size': get_resource_file_size}


    # IActions

    def get_actions(self):
        return {'group_tree': action.group_tree,
                'group_tree_section': action.group_tree_section,
        }


class HierarchyForm(plugins.SingletonPlugin, DefaultOrganizationForm):
    plugins.implements(plugins.IGroupForm, inherit=True)

    # IGroupForm

    def group_types(self):
        return ('organization',)

    def setup_template_variables(self, context, data_dict):
        from pylons import tmpl_context as c

        model = context['model']
        group_id = data_dict.get('id')
        if group_id:
            group = model.Group.get(group_id)
            c.allowable_parent_groups = \
                group.groups_allowed_to_be_its_parent(type='organization')
        else:
            c.allowable_parent_groups = model.Group.all(
                group_type='organization')
