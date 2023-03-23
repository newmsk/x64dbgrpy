from setuptools.command.build_py import build_py
import setuptools
import pkg_resources
import os
import re


# generate py modules from proto files and fix import to relative
# equivalent to
# python -m grpc_tools.protoc -I=. --python_out=src/x64rdbgpy --grpc_python_out=src/x64rdbgpy  proto/*.proto
# fix to relative: from proto import -> from ..proto import

class BuildPy(build_py):
    def run(self):
        from grpc_tools import protoc

        protos_include = pkg_resources.resource_filename(
            'grpc_tools', '_proto')
        package_root = r'.'
        out_path = r'src/x64rdbgpy'
        protos_path = r'proto/*.proto'

        command = [
            'grpc_tools.protoc',
            f'--proto_path={protos_include}',
            f'--proto_path={package_root}',
            f'--python_out={out_path}',
            f'--grpc_python_out={out_path}',
            f'{protos_path}',
        ]

        if protoc.main(command) != 0:
            raise Exception('error: generating proto files failed')

        # create __init__.py
        open(r"src/x64rdbgpy/proto/__init__.py", "w").close()

        for dr, _, files in os.walk(r"src/x64rdbgpy/proto"):
            for file in files:
                if not file.endswith("_pb2.py") and not file.endswith("_pb2_grpc.py"):
                    continue
                path = os.path.join(dr, file)
                with open(path, 'r+', encoding="utf-8") as f:
                    script = f.read()
                    fixed = re.sub(r"from proto import (.*) as (.*)\n", r"from ..proto import \1 as \2\n", script)
                    f.seek(0, os.SEEK_SET)
                    f.write(fixed)

        super(BuildPy, self).run()


if __name__ == "__main__":
    setuptools.setup(
        cmdclass={
            'build_py': BuildPy
        }
    )
