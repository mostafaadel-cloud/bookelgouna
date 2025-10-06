from fabric.api import local, run, env, cd, prefix, task, get, prompt
from fabric.colors import red


@task
def test():
    env.hosts = ['test.bookelgouna.com:2214']
    env.user = 'webmaster'
    env.path = '/home/webmaster/bookelgouna'
    env.backup_folder = '/home/webmaster/backup'
    env.branch = 'master'
    env.sv_group = 'bookelgouna'
    env.settings = 'prod_local'


@task
def prod():
    env.hosts = ['bookelgouna.com']
    env.user = 'webmaster'
    env.path = '/home/webmaster/bookelgouna'
    env.backup_folder = '/home/webmaster/backup'
    env.branch = 'master'
    env.sv_group = 'bookelgouna'
    env.settings = 'prod_local'

env.use_ssh_config = True

ENV_COMMAND = 'source env/bin/activate'


@task
def manage(command, rosetta=False):
    if not rosetta:
        with cd(env.path), prefix(ENV_COMMAND):
            run('python bookelgouna/manage.py {} --settings=config.{}'.format(command, env.settings), shell=False)
    else:
        with cd('{}/bookelgouna'.format(env.path)), prefix('source ../env/bin/activate'):
            run('python manage.py {} --settings=config.{}'.format(command, env.settings), shell=False)


@task
def update():
    with cd(env.path):
        run('git checkout -- bookelgouna/templates/base_site.html')
        run('git pull origin {}'.format(env.branch))
        run('find . -name "*.pyc" -exec rm -f {} \;')
        requirements()
        npm('install')
        grunt('deploy')
        migrate()
        collectstatic()
        make_translations(make=True, compile=True)
        restart()


@task
def requirements():
    with cd(env.path), prefix(ENV_COMMAND):
        run('pip install --exists-action=s --upgrade -r requirements.txt')


@task
def migrate():
    with cd(env.path):
        manage('migrate --no-initial-data')


@task
def collectstatic():
    with cd(env.path):
        manage('collectstatic --noinput')


@task
def grunt(command):
    with cd(env.path):
        run('grunt {}'.format(command))


@task
def npm(command):
    with cd(env.path):
        run('npm {}'.format(command))


@task
def restart():
    run('supervisorctl restart {}:'.format(env.sv_group))


@task
def start():
    run('supervisorctl start {}:'.format(env.sv_group))


@task
def stop():
    run('supervisorctl stop {}:'.format(env.sv_group))


@task
def tail(app):
    run('supervisorctl tail -f {}:{}'.format(env.sv_group, app))


@task
def status():
    run('supervisorctl status')


@task
def make_translations(make=False, compile=False):
    get_translation_files(backup_only=True)

    if (not make) and (not compile):
        print 'Making messages'
        manage('makemessages --all', rosetta=True)
        print 'Compiling messages'
        manage('compilemessages', rosetta=True)
    else:
        if make:
            print 'Making messages'
            manage('makemessages --all', rosetta=True)
        if compile:
            print 'Compiling messages'
            manage('compilemessages', rosetta=True)


@task
def get_translation_files(local_storage=None, backup_only=False):
    with cd(env.path):
        translation_pack = run('date -Iminutes',
                               shell=False, quiet=True
                               )
        folder = '{}/translations'.format(env.backup_folder)
        archive_name = 'translation_pack-{}.tgz'.format(translation_pack)
        full_archive_path = '{}/{}'.format(folder, archive_name)
        run('tar -zcvf {} $(find ./bookelgouna -type f -name "*.po")'.format(full_archive_path),
            shell=False, quiet=True
            )

    if not backup_only:
        if not local_storage:
            local_archive_name = '/tmp/{}'.format(archive_name)
            get(full_archive_path, '/tmp')
        else:
            local_archive_name = '{}/{}'.format(local_storage, archive_name)
            get(full_archive_path, local_storage)

        unpack_choice = prompt(red('This operation will overwrite local files!\nUnpack? y/n'))
        if unpack_choice and unpack_choice.lower() == 'y':
            print 'Unpacking'
            local('tar -zxvf {} -C ./'.format(local_archive_name))
        else:
            print 'Aborting'


@task
def build_solr_schemas():
    manage("build_solr_schemas")


@task
def rebuild_solr_indexes():
    manage("rebuild_solr_indexes")
