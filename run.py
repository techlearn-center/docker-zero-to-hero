#!/usr/bin/env python3
"""
Docker Zero-to-Hero Workshop Grader
====================================
Validates workshop artifacts and calculates your score.

Usage:
    python run.py              # Check all modules and show score
    python run.py --module 4   # Check specific module only
    python run.py --json       # Output results as JSON
"""

import os
import sys
import re
import json
import argparse
import subprocess

# ─── Windows Color Support ─────────────────────────────────────────────────

if sys.platform == "win32":
    os.system("color")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    END = "\033[0m"


def colored(text, color):
    return f"{color}{text}{Colors.END}"


# ─── File Helpers ──────────────────────────────────────────────────────────

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app")


def read_file(path):
    """Read a file and return its contents, or empty string if not found."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, PermissionError):
        return ""


def file_exists(path):
    """Check if a file exists."""
    return os.path.isfile(path)


# ─── Check Functions ───────────────────────────────────────────────────────
# Each returns (passed: bool, message: str)


def check_dockerfile_exists():
    """Module 04: Dockerfile exists in app/ directory"""
    path = os.path.join(APP_DIR, "Dockerfile")
    if file_exists(path):
        content = read_file(path)
        # Check it's not just the starter template
        if "# TODO:" in content and content.count("FROM") <= 1 and "COPY" not in content.split("# TODO")[0].split("FROM")[-1]:
            return False, "Dockerfile exists but appears to be the starter template. Complete the TODO items."
        return True, "Dockerfile found in app/"
    return False, "No Dockerfile found in app/ directory"


def check_dockerfile_from_node():
    """Module 04: Dockerfile uses node base image"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    if re.search(r"FROM\s+node:", content, re.IGNORECASE):
        return True, "Dockerfile uses node base image"
    return False, "Dockerfile should use a node base image (e.g., FROM node:18-alpine)"


def check_dockerfile_workdir():
    """Module 04: Dockerfile sets WORKDIR"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    if re.search(r"WORKDIR\s+/app", content, re.IGNORECASE):
        return True, "WORKDIR set to /app"
    return False, "Dockerfile should set WORKDIR to /app"


def check_dockerfile_copy_package_first():
    """Module 04: Dockerfile copies package.json before source"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    lines = [l.strip() for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]

    copy_indices = []
    for i, line in enumerate(lines):
        if line.upper().startswith("COPY"):
            copy_indices.append((i, line))

    if len(copy_indices) >= 2:
        first_copy = copy_indices[0][1].lower()
        if "package" in first_copy:
            return True, "package.json is copied before source code (good for layer caching)"

    if len(copy_indices) == 1:
        return False, "Use two COPY instructions: copy package.json first, then the rest"

    return False, "Dockerfile should COPY package.json before COPY . ."


def check_dockerfile_run_install():
    """Module 04: Dockerfile runs npm/yarn install"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    if re.search(r"RUN\s+(npm|yarn)\s+install", content, re.IGNORECASE):
        return True, "Dependencies are installed with npm/yarn install"
    return False, "Dockerfile should RUN npm install (or yarn install)"


def check_dockerfile_copy_source():
    """Module 04: Dockerfile copies source code"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    lines = [l.strip() for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]

    copy_count = sum(1 for l in lines if l.upper().startswith("COPY"))
    if copy_count >= 2:
        return True, "Source code is copied into the image"

    if copy_count == 1 and re.search(r"COPY\s+\.\s+\.", content):
        return True, "Source code is copied (single COPY . .)"

    return False, "Dockerfile should COPY source code into the image"


def check_dockerfile_expose():
    """Module 04: Dockerfile exposes port"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    if re.search(r"EXPOSE\s+3000", content, re.IGNORECASE):
        return True, "Port 3000 is exposed"
    return False, "Dockerfile should EXPOSE 3000"


def check_dockerfile_cmd():
    """Module 04: Dockerfile has CMD instruction"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    if re.search(r"CMD\s+", content, re.IGNORECASE):
        return True, "CMD instruction is defined"
    return False, "Dockerfile should have a CMD instruction to start the app"


def check_image_builds():
    """Module 04: Docker image builds successfully"""
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "todo-app-test", os.path.join(APP_DIR)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            # Clean up test image
            subprocess.run(["docker", "rmi", "todo-app-test"], capture_output=True, timeout=30)
            return True, "Docker image builds successfully"
        return False, f"Docker build failed: {result.stderr[:200]}"
    except FileNotFoundError:
        return False, "Docker is not installed or not in PATH"
    except subprocess.TimeoutExpired:
        return False, "Docker build timed out (>120 seconds)"
    except Exception as e:
        return False, f"Could not test Docker build: {str(e)}"


def check_source_modified():
    """Module 05: Source code has been modified from the original"""
    content = read_file(os.path.join(APP_DIR, "src", "static", "index.html"))
    original_text = "No todos yet! Add one above to get started."
    if content and original_text not in content:
        return True, "Source code has been modified from the original"
    if not content:
        return False, "Could not read app/src/static/index.html"
    return False, "Modify the empty state text in app/src/static/index.html (Module 05)"


def check_update_text_changed():
    """Module 05: Empty state text has been updated"""
    content = read_file(os.path.join(APP_DIR, "src", "static", "index.html"))
    if not content:
        return False, "Could not read app/src/static/index.html"

    # Check that the empty-state element exists but with different text
    if 'id="empty-state"' in content:
        original = "No todos yet! Add one above to get started."
        if original not in content:
            return True, "Empty state text has been updated"
        return False, "Change the text inside the empty-state paragraph"

    return False, "The empty-state element should still exist in index.html"


def check_image_tagged():
    """Module 06: Image has been tagged with username/repo format"""
    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.strip().split("\n"):
            if "/" in line and "todo" in line.lower():
                return True, f"Image tagged correctly: {line}"
        return False, "No image found with username/repository format containing 'todo'"
    except Exception:
        return False, "Could not check Docker images (is Docker running?)"


def check_tag_format():
    """Module 06: Image tag follows proper naming convention"""
    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.strip().split("\n"):
            if re.match(r"^[\w\-]+/[\w\-]+:\w+", line):
                if "todo" in line.lower():
                    return True, f"Tag format is valid: {line}"
        return False, "Tag should follow format: username/repository:tag"
    except Exception:
        return False, "Could not check Docker images"


def check_volume_config():
    """Module 07: Volume configuration is present"""
    # Check docker-compose.yml for volume config
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))
    dockerfile = read_file(os.path.join(APP_DIR, "Dockerfile"))

    if "todo-db" in compose or "todo-mysql-data" in compose:
        if "volumes:" in compose:
            return True, "Volume configuration found in docker-compose.yml"

    # Also accept if they've been running docker commands with volumes
    try:
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=30
        )
        if "todo" in result.stdout.lower():
            return True, "Docker volume found for todo app"
    except Exception:
        pass

    return False, "Configure a named volume for data persistence (Module 07)"


def check_volume_mount_path():
    """Module 07: Volume mount path is correct"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    # Check for proper mount paths
    if "/var/lib/mysql" in compose or "/app/data" in compose:
        return True, "Volume mount path is correctly configured"

    # Check if a todo-related volume exists
    try:
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=30
        )
        volumes = result.stdout.strip().split("\n")
        todo_volumes = [v for v in volumes if "todo" in v.lower()]
        if todo_volumes:
            return True, f"Volume(s) found: {', '.join(todo_volumes)}"
    except Exception:
        pass

    return False, "Mount path should point to the database data directory"


def check_bind_mount_config():
    """Module 08: Bind mount configuration understood"""
    # This checks if the user has a proper development setup understanding
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    # Check for bind mount syntax in compose or evidence of usage
    if "./" in compose and ":/app" in compose:
        return True, "Bind mount configuration found"

    # Check app/Dockerfile for development-related instructions
    dockerfile = read_file(os.path.join(APP_DIR, "Dockerfile"))
    if "nodemon" in dockerfile.lower() or "dev" in dockerfile.lower():
        return True, "Development configuration found"

    # Give credit if they have a proper compose file with build context
    if "build:" in compose and "./app" in compose:
        return True, "Build context configured (implies understanding of bind mounts)"

    return False, "Set up a bind mount for development workflow (Module 08)"


def check_bind_mount_dev():
    """Module 08: Development workflow configured"""
    # Check package.json for dev script
    pkg = read_file(os.path.join(APP_DIR, "package.json"))
    if '"dev"' in pkg and "nodemon" in pkg:
        return True, "Development script with nodemon is configured"
    return False, "package.json should have a 'dev' script using nodemon"


def check_mysql_host_env():
    """Module 09: MYSQL_HOST environment variable configured"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))
    if "MYSQL_HOST" in compose:
        return True, "MYSQL_HOST environment variable is set"
    return False, "Set MYSQL_HOST environment variable in docker-compose.yml"


def check_mysql_credentials():
    """Module 09: MySQL credentials configured"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))
    has_user = "MYSQL_USER" in compose
    has_password = "MYSQL_PASSWORD" in compose or "MYSQL_ROOT_PASSWORD" in compose
    has_db = "MYSQL_DB" in compose or "MYSQL_DATABASE" in compose

    if has_user and has_password and has_db:
        return True, "MySQL credentials are configured"

    missing = []
    if not has_user:
        missing.append("MYSQL_USER")
    if not has_password:
        missing.append("MYSQL_PASSWORD/MYSQL_ROOT_PASSWORD")
    if not has_db:
        missing.append("MYSQL_DB/MYSQL_DATABASE")

    return False, f"Missing MySQL env vars: {', '.join(missing)}"


def check_multi_container_network():
    """Module 09: Multi-container networking configured"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    # In Compose, services on the same file share a default network
    has_app = re.search(r"^\s+app:", compose, re.MULTILINE)
    has_mysql = re.search(r"^\s+mysql:", compose, re.MULTILINE)

    if has_app and has_mysql:
        return True, "Multi-container setup with app and mysql services"

    if has_app:
        return False, "Add a 'mysql' service to docker-compose.yml"

    return False, "Configure both app and mysql services in docker-compose.yml"


def check_compose_file_exists():
    """Module 10: docker-compose.yml exists and has content"""
    path = os.path.join(ROOT_DIR, "docker-compose.yml")
    if file_exists(path):
        content = read_file(path)
        if "services:" in content and "# TODO:" not in content.split("services:")[1][:100]:
            return True, "docker-compose.yml found with service definitions"
        if "services:" in content:
            return True, "docker-compose.yml found (may still have TODOs to complete)"
        return False, "docker-compose.yml exists but doesn't define any services"
    return False, "No docker-compose.yml found in project root"


def check_compose_app_service():
    """Module 10: App service defined in docker-compose.yml"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    has_app = re.search(r"^\s+(app|web):", compose, re.MULTILINE)
    has_build = "build:" in compose

    if has_app and has_build:
        return True, "App service with build configuration defined"
    if has_app:
        return False, "App service exists but needs 'build:' directive"
    return False, "Define a 'web' (or 'app') service in docker-compose.yml"


def check_compose_mysql_service():
    """Module 10: MySQL service defined in docker-compose.yml"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    has_mysql = re.search(r"^\s+mysql:", compose, re.MULTILINE)
    has_image = "mysql:8" in compose or "mysql:latest" in compose

    if has_mysql and has_image:
        return True, "MySQL service with image defined"
    if has_mysql:
        return True, "MySQL service defined"
    return False, "Define a 'mysql' service using the mysql:8.0 image"


def check_compose_volumes():
    """Module 10: Named volume defined in docker-compose.yml"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    # Check for top-level volumes section
    lines = compose.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("volumes:") and not line.startswith("  "):
            return True, "Named volumes defined at top level"

    return False, "Define named volumes at the top level of docker-compose.yml"


def check_compose_ports():
    """Module 10: Port mapping defined for app service"""
    compose = read_file(os.path.join(ROOT_DIR, "docker-compose.yml"))

    if re.search(r"ports:\s*\n\s+-\s*[\"']?3000:3000", compose):
        return True, "Port 3000:3000 mapped for app service"
    if "3000:3000" in compose:
        return True, "Port 3000 mapping found"
    return False, "Map port 3000:3000 in the app service"


def check_multistage_dockerfile():
    """Module 11: Multi-stage Dockerfile"""
    content = read_file(os.path.join(APP_DIR, "Dockerfile"))
    from_count = len(re.findall(r"^FROM\s+", content, re.MULTILINE | re.IGNORECASE))

    if from_count >= 2:
        return True, f"Multi-stage build detected ({from_count} stages)"
    return False, "Use multiple FROM statements for a multi-stage build (Module 11)"


def check_dockerignore():
    """Module 11: .dockerignore file exists"""
    path = os.path.join(APP_DIR, ".dockerignore")
    if file_exists(path):
        content = read_file(path)
        if "node_modules" in content:
            return True, ".dockerignore found with node_modules excluded"
        return True, ".dockerignore found"
    return False, "Create app/.dockerignore to exclude unnecessary files from build context"


# ─── Checks Registry ──────────────────────────────────────────────────────

CHECKS = [
    # Module 04: Containerize an Application (25 pts)
    {"name": "Dockerfile exists", "func": check_dockerfile_exists, "points": 5, "module": 4},
    {"name": "FROM node base image", "func": check_dockerfile_from_node, "points": 3, "module": 4},
    {"name": "WORKDIR set to /app", "func": check_dockerfile_workdir, "points": 2, "module": 4},
    {"name": "COPY package.json first", "func": check_dockerfile_copy_package_first, "points": 3, "module": 4},
    {"name": "RUN npm/yarn install", "func": check_dockerfile_run_install, "points": 3, "module": 4},
    {"name": "COPY source code", "func": check_dockerfile_copy_source, "points": 2, "module": 4},
    {"name": "EXPOSE 3000", "func": check_dockerfile_expose, "points": 2, "module": 4},
    {"name": "CMD defined", "func": check_dockerfile_cmd, "points": 3, "module": 4},
    {"name": "Image builds successfully", "func": check_image_builds, "points": 2, "module": 4},

    # Module 05: Update the Application (10 pts)
    {"name": "Source code modified", "func": check_source_modified, "points": 5, "module": 5},
    {"name": "Empty state text changed", "func": check_update_text_changed, "points": 5, "module": 5},

    # Module 06: Share the Application (10 pts)
    {"name": "Image tagged correctly", "func": check_image_tagged, "points": 5, "module": 6},
    {"name": "Tag format valid", "func": check_tag_format, "points": 5, "module": 6},

    # Module 07: Persist the DB (10 pts)
    {"name": "Volume config present", "func": check_volume_config, "points": 5, "module": 7},
    {"name": "Volume mount path correct", "func": check_volume_mount_path, "points": 5, "module": 7},

    # Module 08: Use Bind Mounts (10 pts)
    {"name": "Bind mount configured", "func": check_bind_mount_config, "points": 5, "module": 8},
    {"name": "Dev workflow configured", "func": check_bind_mount_dev, "points": 5, "module": 8},

    # Module 09: Multi-Container Apps (15 pts)
    {"name": "MYSQL_HOST env var", "func": check_mysql_host_env, "points": 5, "module": 9},
    {"name": "MySQL credentials", "func": check_mysql_credentials, "points": 5, "module": 9},
    {"name": "Multi-container network", "func": check_multi_container_network, "points": 5, "module": 9},

    # Module 10: Use Docker Compose (15 pts)
    {"name": "Compose file exists", "func": check_compose_file_exists, "points": 3, "module": 10},
    {"name": "App service defined", "func": check_compose_app_service, "points": 3, "module": 10},
    {"name": "MySQL service defined", "func": check_compose_mysql_service, "points": 3, "module": 10},
    {"name": "Volumes defined", "func": check_compose_volumes, "points": 3, "module": 10},
    {"name": "Ports mapped", "func": check_compose_ports, "points": 3, "module": 10},

    # Module 11: Image-Building Best Practices (5 pts)
    {"name": "Multi-stage Dockerfile", "func": check_multistage_dockerfile, "points": 3, "module": 11},
    {"name": ".dockerignore exists", "func": check_dockerignore, "points": 2, "module": 11},
]


# ─── Display Helpers ───────────────────────────────────────────────────────

def print_header():
    print()
    print(colored("=" * 60, Colors.CYAN))
    print(colored("  Docker Zero-to-Hero Workshop Grader", Colors.BOLD))
    print(colored("=" * 60, Colors.CYAN))
    print()


def print_progress_bar(earned, total):
    bar_width = 40
    filled = int(bar_width * earned / total)
    bar = "█" * filled + "░" * (bar_width - filled)
    percentage = (earned / total) * 100

    color = Colors.RED
    if percentage >= 70:
        color = Colors.GREEN
    elif percentage >= 40:
        color = Colors.YELLOW

    print(f"\n  Progress: {colored(bar, color)} {colored(f'{earned}/{total}', Colors.BOLD)} ({percentage:.0f}%)")
    print()


def print_module_header(module_num):
    module_names = {
        4: "Containerize an Application",
        5: "Update the Application",
        6: "Share the Application",
        7: "Persist the DB",
        8: "Use Bind Mounts",
        9: "Multi-Container Apps",
        10: "Use Docker Compose",
        11: "Image-Building Best Practices",
    }
    name = module_names.get(module_num, f"Module {module_num:02d}")
    print(colored(f"  Module {module_num:02d}: {name}", Colors.BOLD))
    print(colored(f"  {'─' * 50}", Colors.DIM))


# ─── Main ──────────────────────────────────────────────────────────────────

def run_checks(module_filter=None):
    print_header()

    total_points = 0
    earned_points = 0
    results = []
    current_module = None

    checks_to_run = CHECKS
    if module_filter is not None:
        checks_to_run = [c for c in CHECKS if c["module"] == module_filter]
        if not checks_to_run:
            print(colored(f"  No graded checks for module {module_filter}", Colors.YELLOW))
            return

    for check in checks_to_run:
        module = check["module"]

        if module != current_module:
            if current_module is not None:
                print()
            print_module_header(module)
            current_module = module

        total_points += check["points"]

        try:
            passed, message = check["func"]()
        except Exception as e:
            passed, message = False, f"Error: {str(e)}"

        if passed:
            earned_points += check["points"]
            icon = colored("✓", Colors.GREEN)
            pts = colored(f"+{check['points']}pts", Colors.GREEN)
        else:
            icon = colored("✗", Colors.RED)
            pts = colored(f" {check['points']}pts", Colors.DIM)

        print(f"    {icon} {check['name']:.<40} {pts}")
        if not passed:
            print(colored(f"      └─ {message}", Colors.DIM))

        results.append({
            "name": check["name"],
            "module": check["module"],
            "points": check["points"],
            "earned": check["points"] if passed else 0,
            "passed": passed,
            "message": message,
        })

    print_progress_bar(earned_points, total_points)

    # Pass/Fail status
    passing_score = 70
    if earned_points >= passing_score:
        print(colored(f"  🎉 PASSED! You scored {earned_points}/{total_points} (need {passing_score} to pass)", Colors.GREEN))
    else:
        remaining = passing_score - earned_points
        print(colored(f"  Keep going! You need {remaining} more points to pass ({passing_score}/{total_points})", Colors.YELLOW))

    print()
    return results, earned_points, total_points


def main():
    parser = argparse.ArgumentParser(description="Docker Zero-to-Hero Workshop Grader")
    parser.add_argument("--module", type=int, help="Check a specific module only (e.g., --module 4)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    results, earned, total = run_checks(module_filter=args.module)

    if args.json:
        output = {
            "total_points": total,
            "earned_points": earned,
            "passing_score": 70,
            "passed": earned >= 70,
            "checks": results,
        }
        json_path = os.path.join(ROOT_DIR, "results.json")
        with open(json_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"  Results written to {json_path}")


if __name__ == "__main__":
    main()
