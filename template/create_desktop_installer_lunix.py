
import os, shutil
import PyInstaller.__main__

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

# my spec file in "dev\config" dir
workdir = os.getcwd()
# fn_msi_spec = os.path.join(workdir, 'main_msi.spec')

# define the "dev\dist" and "dev\build" dirs
# os.chdir("..")
name = 'Flask BDA'
devdir = os.getcwd()
distdir = os.path.join(devdir, '../desktop_lunix/dist',name)
builddir = os.path.join(devdir, '../desktop_lunix/build')

# call pyinstaller directly
PyInstaller.__main__.run([
    'run_desktop.py',
    '--distpath', distdir,
    '--workpath', builddir,
    '--onefile',
    '--noconsole',
    '--windowed',
    '--clean',
    '--add-data', 'app;app',
    # '--add-data', 'databases;databases',
    # '--add-data', 'config.py;./',
    '--add-data', 'FLASK-BDA LICENSE;./',
    '--add-data', 'LICENSE;./',
    '--hidden-import', 'engineio.async_drivers',
    '--hidden-import', 'pyodbc',
    '--icon', './app/static/images/icon.ico',
    '--debug','False',
    '--log-level','WARN', # LEVEL may be one of TRACE, DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
    '--key', '1234567890123456', # The key used to encrypt Python bytecode.
    '--name', name,
    ])

copy_config_to_dir = '{0}/config.py'.format(distdir)
copy_license_to_dir = '{0}/LICENSE'.format(distdir)
copy_flask_license_to_dir = '{0}/FLASK-BDA LICENSE'.format(distdir)
copy_databases_to_dir = '{0}/databases'.format(distdir)

shutil.copy2('config.py', copy_config_to_dir)
shutil.copy2('LICENSE', copy_license_to_dir)
shutil.copy2('FLASK-BDA LICENSE', copy_flask_license_to_dir)

copytree('databases',copy_databases_to_dir)

