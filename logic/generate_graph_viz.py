import json
import os

def generate_mermaid():
    print("Generating Graph Visualization...")
    extracts_dir = "extracts"
    static_graph_path = os.path.join("sovereign_engine", "data", "graph.json")
    
    mermaid = "graph TD\n"
    mermaid += "  ROOT[Sovereign Knowledge Graph] --> Space\n"
    mermaid += "  ROOT --> Network\n"
    mermaid += "  ROOT --> Trade\n"
    mermaid += "  ROOT --> Forensic[Forensic Evidence]\n"
    
    # 1. Add Static Nodes and Edges
    if os.path.exists(static_graph_path):
        with open(static_graph_path, 'r') as f:
            static_data = json.load(f)
            # Add nodes
            for node in static_data.get('nodes', []):
                node_id = node['id'].replace('-', '_')
                mermaid += f"  Forensic --> {node_id}[\"{node['claim'][:50]}...\"]\n"
            
            # Add edges
            for edge in static_data.get('edges', []):
                from_id = edge['from'].replace('-', '_')
                to_id = edge['to'].replace('-', '_')
                mermaid += f"  {from_id} -- \"{edge['rel']}\" --> {to_id}\n"

    # 2. Add Dynamic Signal Nodes
    if os.path.exists(extracts_dir):
        files = [f for f in os.listdir(extracts_dir) if f.endswith('.json')]
        for f in files[:20]: # Limit for clarity
            node_name = f.replace('.json','').replace('-','_')
            if "space" in f or "neo" in f:
                mermaid += f"  Space --> {node_name}\n"
            elif "bgp" in f or "network" in f:
                mermaid += f"  Network --> {node_name}\n"
            elif "sea" in f or "deep_sea" in f or "trade" in f:
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
