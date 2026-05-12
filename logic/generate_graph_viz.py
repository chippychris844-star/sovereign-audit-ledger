import json
import os

def generate_mermaid():
    print("Generating Graph Visualization...")
    extracts_dir = "extracts"
    if not os.path.exists(extracts_dir):
        return
    
    files = [f for f in os.listdir(extracts_dir) if f.endswith('.json')]
    
    mermaid = "graph TD\n"
    mermaid += "  ROOT[Sovereign Knowledge Graph] --> Space\n"
    mermaid += "  ROOT --> Network\n"
    mermaid += "  ROOT --> Trade\n"
    
    # Simple logic to link latest files to categories
    for f in files[:20]: # Limit for clarity
        node_name = f.replace('.json','').replace('-','_')
        if "space" in f or "neo" in f:
            mermaid += f"  Space --> {node_name}\n"
        elif "bgp" in f or "network" in f:
            mermaid += f"  Network --> {node_name}\n"
        elif "sea" in f or "deep_sea" in f:
            mermaid += f"  Trade --> {node_name}\n"
            
    with open("graph.mermaid", "w") as f:
        f.write(mermaid)
        
    # Update README
    readme_path = "README.md"
    content = "# Sovereign Audit Ledger\n\n## Current Knowledge Graph Status\n\n```mermaid\n" + mermaid + "```\n"
    with open(readme_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    generate_mermaid()
