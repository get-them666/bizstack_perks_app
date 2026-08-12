import os

dashboard_path = "/Users/shaunoleary/bizstack_perks_app/dashboard.py"

if os.path.exists(dashboard_path):
    with open(dashboard_path, "r") as f:
        content = f.read()
    
    # Inject your new production link into the main presentation header
    updated_content = content.replace(
        'st.title("📊 BizStack Perks App — Executive Lead & Underwriting Monitor")',
        'st.title("📊 BizStack Perks App — Executive Lead & Underwriting Monitor")\nst.caption("🌐 Public Landing Page: [bizstack-perks-hub.surge.sh](http://bizstack-perks-hub.surge.sh)")'
    )
    
    with open(dashboard_path, "w") as f:
        f.write(updated_content)
    print("[SUCCESS] Dashboard title updated with your live web URL.")
else:
    print("[ERROR] dashboard.py not found at path.")
