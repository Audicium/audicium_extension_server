from src.utils.script_loader import ScriptLoader

if __name__ == '__main__':
    s_loader = ScriptLoader()
    s_loader.load_script(module_name='test_scripts.test',
                         path=r'D:\Dev\Flutter\audicium project\audicium_project\extension_server\extension_server\test_scripts\test.py')

    if not s_loader.is_loaded():
        print('not loaded')

    print(s_loader.get_home_page())
