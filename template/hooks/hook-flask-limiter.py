from PyInstaller.utils.hooks import collect_all


def hook(hook_api):
    packages = [
        'click',
        'flask',
        'Flask-Limiter'
        'itsdangerous'
        'Jinja2'
        'limits'
        'MarkupSafe'
        'six'
        'Werkzeug'
    ]
    for package in packages:
        datas, binaries, hiddenimports = collect_all(package)
        hook_api.add_datas(datas)
        hook_api.add_binaries(binaries)
        hook_api.add_imports(*hiddenimports)