from PyInstaller.utils.hooks import collect_all, copy_metadata, collect_data_files


def hook(hook_api):
    packages = [
        'click',
        'flask',
        'Flask-Limiter',
        'itsdangerous',
        'Jinja2',
        'limits',
        'MarkupSafe',
        'six',
        'Werkzeug'
    ]
    for package in packages:
        datas, binaries, hiddenimports = collect_all(package)

        # datas += copy_metadata(package)
        # datas += collect_data_files(package)

        print"(------------------------------------------------------------------------------------")
        print"(------------------------------------------------------------------------------------")
        print"(---------------------------- LOADING PACKAGE: " + str(package) +" ----------------------------")
        print"(------------------------------------------------------------------------------------")
        print"(------------------------------------------------------------------------------------")

        hook_api.add_datas(datas)
        hook_api.add_binaries(binaries)
        hook_api.add_imports(*hiddenimports)