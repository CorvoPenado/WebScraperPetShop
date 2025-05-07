from setuptools import setup, Extension
from Cython.Build import cythonize
import os

def get_py_files():
    py_files = []
    for root, dirs, files in os.walk('bot'):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file).replace('\\', '/')
                # Create Extension object for each file
                extension = Extension(
                    name=file_path.replace('/', '.').replace('.py', ''),
                    sources=[file_path],
                    # Add compiler and linker arguments for proper encoding
                    extra_compile_args=['/utf-8'] if os.name == 'nt' else ['-O2'],
                )
                py_files.append(extension)
    return py_files

setup(
    ext_modules=cythonize(
        get_py_files(),
        compiler_directives={
            'language_level': '3',
            'embedsignature': True,
            # Removed 'encoding' directive
        },
        force=True
    )
)