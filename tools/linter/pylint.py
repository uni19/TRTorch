import os
import sys
import glob
import utils
import subprocess
import yapf
import pwd

VALID_PY_FILE_TYPES = [".py"]


def lint(user, target_files, conf, change_file=True):
    return yapf.FormatFiles(
        filenames=target_files,
        lines=None,
        style_config=conf,
        no_local_style=None,
        in_place=change_file,
        print_diff=False,
        verify=True,
        parallel=True,
        verbose=True)


if __name__ == "__main__":
    BAZEL_ROOT = utils.find_bazel_root()
    STYLE_CONF_PATH = BAZEL_ROOT + "/.style.yapf"
    USER = pwd.getpwuid(os.getuid())[0]
    projects = utils.CHECK_PROJECTS(sys.argv[1:])
    if "//..." in projects:
        projects = [p.replace(BAZEL_ROOT, "/")[:-1] for p in glob.glob(BAZEL_ROOT + '/*/')]
        projects = [p for p in projects if p not in utils.BLACKLISTED_BAZEL_TARGETS]

    for p in projects:
        if p.endswith("/..."):
            p = p[:-4]
        path = BAZEL_ROOT + '/' + p[2:]
        files = utils.glob_files(path, VALID_PY_FILE_TYPES)
        if files != []:
            changed = lint(USER, files, STYLE_CONF_PATH)
            if changed:
                print(
                    "\033[93mWARNING:\033[0m This command modified your files with the recommended linting, you should review the changes before committing"
                )
                sys.exit(1)
