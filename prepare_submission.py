"""
GitHub Submission Preparation Script
Run this before pushing to GitHub to ensure everything is ready
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def print_section(title, symbol="="):
    print(f"\n{symbol * 70}")
    print(f"  {title}")
    print(f"{symbol * 70}\n")

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    status = "✅" if exists else ("❌" if required else "⚠️ ")
    print(f"{status} {filepath}")
    return exists

def check_env_file():
    """Verify .env is not included but .env.example is"""
    print_section("Environment Files Check")
    
    env_exists = Path(".env").exists()
    example_exists = Path(".env.example").exists()
    
    if env_exists:
        print("❌ .env file exists - MUST NOT be committed!")
        print("   Add .env to .gitignore")
        return False
    else:
        print("✅ .env file not present (good - contains secrets)")
    
    if example_exists:
        print("✅ .env.example exists (template for users)")
    else:
        print("❌ .env.example missing - users need this template")
        return False
    
    return True

def check_required_files():
    """Check all required files are present"""
    print_section("Required Files Check")
    
    required = [
        "README.md",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
        ".env.example",
        "main.py",
        "SETUP.md",
        "QUICKSTART.md",
        "CERTIFICATE_CHECKLIST.md",
    ]
    
    all_present = True
    for file in required:
        if not check_file_exists(file, required=True):
            all_present = False
    
    return all_present

def check_optional_files():
    """Check optional but recommended files"""
    print_section("Optional Files Check")
    
    optional = [
        "SLACK_INTEGRATION.md",
        "demo.py",
        "VIDEO_SCRIPT.md",
        "recreate_agent.py",
        "update_agent.py",
    ]
    
    for file in optional:
        check_file_exists(file, required=False)

def check_directory_structure():
    """Verify directory structure"""
    print_section("Directory Structure Check")
    
    required_dirs = [
        "src",
        "src/agents",
        "src/data_ingestion",
        "src/tools",
        "src/utils",
        "ui",
        "data",
        "data/raw",
        "logs",
    ]
    
    all_present = True
    for dir_path in required_dirs:
        exists = Path(dir_path).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {dir_path}/")
        if not exists:
            all_present = False
    
    return all_present

def check_data_files():
    """Check data sources are present"""
    print_section("Data Sources Check")
    
    csv_file = "data/raw/sample_policies.csv"
    scraped_dir = "data/raw/scraped_policies"
    
    csv_exists = Path(csv_file).exists()
    scraped_exists = Path(scraped_dir).exists()
    
    if csv_exists:
        # Check if has content
        import pandas as pd
        try:
            df = pd.read_csv(csv_file)
            print(f"✅ {csv_file} ({len(df)} policies)")
        except:
            print(f"⚠️  {csv_file} (unable to read)")
    else:
        print(f"❌ {csv_file} missing")
    
    if scraped_exists:
        json_file = Path(scraped_dir) / "scraped_policies.json"
        if json_file.exists():
            print(f"✅ {scraped_dir}/scraped_policies.json")
        else:
            print(f"⚠️  {scraped_dir}/ exists but no scraped_policies.json")
    else:
        print(f"❌ {scraped_dir}/ missing")
    
    return csv_exists and scraped_exists

def check_readme_content():
    """Verify README has required sections"""
    print_section("README Content Check")
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        required_sections = [
            ("Demo Video", "🎥" or "demo" in content.lower()),
            ("Quick Start", "quick start" in content.lower()),
            ("Architecture", "architecture" in content.lower()),
            ("Certificate Requirements", "certificate" in content.lower()),
            ("Tool Integration", "tool" in content.lower()),
            ("Future Improvements", "future" in content.lower()),
            ("Data Sources", "data source" in content.lower()),
        ]
        
        all_present = True
        for section, _ in required_sections:
            present = section.lower() in content.lower()
            status = "✅" if present else "❌"
            print(f"{status} {section} section")
            if not present:
                all_present = False
        
        # Check for placeholder text
        if "YOUR_USERNAME" in content:
            print("⚠️  Update YOUR_USERNAME placeholder in README")
        if "YOUR_VIDEO_LINK_HERE" in content:
            print("⚠️  Add demo video link to README")
        
        return all_present
    except Exception as e:
        print(f"❌ Error reading README.md: {e}")
        return False

def check_sensitive_data():
    """Check for accidentally committed sensitive data"""
    print_section("Sensitive Data Check")
    
    # Check .env is in .gitignore
    try:
        with open(".gitignore", "r") as f:
            gitignore = f.read()
        
        if ".env" in gitignore:
            print("✅ .env is in .gitignore")
        else:
            print("❌ Add .env to .gitignore!")
            return False
    except:
        print("⚠️  .gitignore not found")
        return False
    
    # Check for API keys in code (actual secrets, not templates)
    sensitive_patterns = [
        ("xoxb-", "Slack bot token"),  # Slack bot token
        ("sk-proj-", "OpenAI key"),    # OpenAI key
        ("AIXPLAIN_API_KEY=\"", "API key"),  # Direct assignment
    ]
    
    print("\nScanning for hardcoded credentials...")
    found_issues = False
    
    # Files to skip entirely (contain example patterns)
    skip_files = {"prepare_submission.py", "GITHUB_SETUP.md"}
    
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".cache", "venv", "env", "logs"]]
        
        for file in files:
            if file in skip_files:
                continue
                
            if file.endswith((".py", ".md", ".txt")):
                filepath = Path(root) / file
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    
                    for i, line in enumerate(lines, 1):
                        # Skip comments and template strings
                        if line.strip().startswith("#"):
                            continue
                        if "os.getenv" in line or "os.environ" in line:
                            continue
                        if "your_" in line.lower() or "your-" in line.lower():
                            continue
                        if "example" in line.lower() or "placeholder" in line.lower():
                            continue
                            
                        for pattern, name in sensitive_patterns:
                            if pattern in line:
                                print(f"⚠️  Found potential {name} in {filepath}:{i}")
                                print(f"    {line.strip()[:80]}")
                                found_issues = True
                except:
                    pass
    
    if not found_issues:
        print("✅ No hardcoded credentials found")
    
    return not found_issues

def generate_checklist():
    """Generate final submission checklist"""
    print_section("Final Submission Checklist", "=")
    
    checklist = [
        ("All required files present", True),
        ("Directory structure correct", True),
        ("Data sources included", True),
        ("README complete with video link", False),  # User must add video
        (".env file excluded", True),
        (".env.example included", True),
        ("No sensitive data in code", True),
        ("LICENSE file present", True),
        ("requirements.txt up to date", True),
        ("Demo video recorded (2-3 min)", False),  # User must create
        ("GitHub repo created and public", False),  # User must do
        ("All placeholders updated", False),  # User must update
    ]
    
    print("Before submitting to devrel@aixplain.com:\n")
    
    for item, auto_check in checklist:
        status = "✅" if auto_check else "[ ]"
        print(f"{status} {item}")
    
    print("\n" + "="*70)
    print("\n🚀 Next Steps:")
    print("1. Update YOUR_USERNAME in README.md")
    print("2. Record demo video (2-3 minutes)")
    print("3. Upload video and add link to README")
    print("4. Create public GitHub repository")
    print("5. Push all code: git add . && git commit -m 'Initial commit' && git push")
    print("6. Send submission email to devrel@aixplain.com")
    print("\n" + "="*70 + "\n")

def main():
    print_section("🎓 Certificate Project - GitHub Submission Preparation", "=")
    
    print("This script checks if your project is ready for submission.\n")
    
    # Run all checks
    checks = {
        "Environment Files": check_env_file(),
        "Required Files": check_required_files(),
        "Directory Structure": check_directory_structure(),
        "Data Sources": check_data_files(),
        "README Content": check_readme_content(),
        "Sensitive Data": check_sensitive_data(),
    }
    
    # Check optional files (doesn't affect pass/fail)
    check_optional_files()
    
    # Summary
    print_section("Summary")
    
    all_passed = all(checks.values())
    
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    if all_passed:
        print("\n✅ All automated checks passed!")
        print("   Your project is ready for manual review and submission.")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return 1
    
    # Generate final checklist
    generate_checklist()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
