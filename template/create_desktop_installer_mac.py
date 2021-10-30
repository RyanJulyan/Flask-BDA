
import os
import PyInstaller.__main__

# my spec file in "dev\config" dir
workdir = os.getcwd()
# fn_msi_spec = os.path.join(workdir, 'main_msi.spec')

# define the "dev\dist" and "dev\build" dirs
# os.chdir("..")
name = 'Flask BDA'
devdir = os.getcwd()
distdir = os.path.join(devdir, '../desktop_mac/dist')
builddir = os.path.join(devdir, '../desktop_mac/build')

# call pyinstaller directly
PyInstaller.__main__.run([
    'run_desktop.py',
    '--distpath', distdir,
    '--workpath', builddir,
    # '--onefile',
    '--noconsole',
    '--windowed',
    '--noconfirm',
    '--clean',
    '--add-data', 'app:app',
    '--add-data', 'databases:databases',
    '--add-data', 'config.py:./',
    '--add-data', 'FLASK-BDA LICENSE:./',
    '--add-data', 'LICENSE:./',
    '--hidden-import', 'engineio.async_drivers',
    '--hidden-import', 'pyodbc',
    '--hidden-import', 'Werkzeug',
    '--hidden-import', 'cmath',
    '--additional-hooks-dir', './pyinstaller_hooks/',
    '--icon', './app/static/images/icon.icns',
    # '--log-level','WARN', # LEVEL may be one of TRACE, DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
    '--key', '1234567890123456', # The key used to encrypt Python bytecode.
    '--name', name,
    ])