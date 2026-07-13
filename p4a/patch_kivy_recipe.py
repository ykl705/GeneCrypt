import os
import sys
import subprocess


def find_recipe_path():
    """Find the kivy recipe __init__.py file in p4a installation."""
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        return sys.argv[1]

    buildozer_dir = os.path.expanduser("~/.buildozer")
    if not os.path.isdir(buildozer_dir):
        print("ERROR: ~/.buildozer not found")
        sys.exit(1)

    r = subprocess.run(
        ["find", buildozer_dir, "-path", "*/recipes/kivy/__init__.py"],
        capture_output=True, text=True
    )
    paths = r.stdout.strip().split("\n")
    if paths and paths[0]:
        return paths[0]

    print("ERROR: Kivy recipe not found")
    sys.exit(1)


def patch_recipe(recipe_path):
    """Patch the kivy recipe to:
    1. Allow Cython >= 3.1.0 (needed for Python 3.14)
    2. Delete pre-compiled .c files before building (forces regeneration with new Cython)
    """
    print(f"Patching kivy recipe at: {recipe_path}")

    with open(recipe_path) as f:
        content = f.read()

    # 1. Update hostpython_prerequisites for Python 3.14 compatibility
    old_prereq = 'hostpython_prerequisites = ["cython>=0.29.1,<=3.0.12"]'
    new_prereq = 'hostpython_prerequisites = ["cython>=3.1.0,<3.3"]'
    if old_prereq in content:
        content = content.replace(old_prereq, new_prereq)
        print("  Updated hostpython_prerequisites to cython>=3.1.0")
    else:
        print("  WARNING: Could not find hostpython_prerequisites - already patched?")

    # 2. Add prebuild_arch method that deletes pre-compiled .c files
    method = (
        "\n    def prebuild_arch(self, arch):\n"
        "        super().prebuild_arch(arch)\n"
        "        import os as _os, fnmatch as _fnmatch\n"
        "        from pythonforandroid.logger import info as _info\n"
        "        build_dir = self.get_build_dir(arch.arch)\n"
        "        if build_dir and _os.path.isdir(build_dir):\n"
        "            deleted = 0\n"
        "            for root, dirs, files in _os.walk(build_dir):\n"
        "                for f in _fnmatch.filter(files, '*.c'):\n"
        "                    _os.remove(_os.path.join(root, f))\n"
        "                    deleted += 1\n"
        "            if deleted:\n"
        '                _info(f"Kivy recipe: deleted {deleted} pre-compiled .c files")\n'
    )

    if method.strip() not in content:
        if "recipe = KivyRecipe()" in content:
            content = content.replace(
                "recipe = KivyRecipe()",
                method + "\n\nrecipe = KivyRecipe()"
            )
            print("  Added .c file deletion to prebuild_arch")
        else:
            print("  WARNING: Could not find 'recipe = KivyRecipe()' marker")
    else:
        print("  prebuild_arch already patched, skipping")

    with open(recipe_path, 'w') as f:
        f.write(content)

    print("Kivy recipe patched successfully")


if __name__ == '__main__':
    recipe_path = find_recipe_path()
    patch_recipe(recipe_path)
