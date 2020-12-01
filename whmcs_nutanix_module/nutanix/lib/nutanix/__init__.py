import importlib
import pkgutil
import os
from .httpClient import CalmClient


def init_calm_env(params):
    os.environ['CALM_DSL_PC_IP'] = params.get('serverip', '')
    os.environ['CALM_DSL_PC_PORT'] = '9440'
    os.environ['CALM_DSL_PC_USERNAME'] = params.get('serverusername', '')
    os.environ['CALM_DSL_PC_PASSWORD'] = params.get('serverpassword', '')
    os.environ['CALM_DSL_DEFAULT_PROJECT'] = 'default'


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    modules = []
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        modules.append(name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return modules


# generate a list of submodules names to verify before eval
allowed_modules = import_submodules(__name__)