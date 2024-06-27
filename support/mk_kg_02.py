from pyvis.network import Network
import networkx as nx
from jinja2 import Template
import json

# Load concepts from a JSON file
with open('test.json', 'r') as file:
    concepts = json.load(file)

# Initialize the graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for category, subcategories in concepts.items():
    G.add_node(category, color="#0000FF", layer="Category", group=category)
    if isinstance(subcategories, dict):
        for subcategory, details in subcategories.items():
            G.add_node(subcategory, color="#00FF00", layer="Subcategory", group=category)
            G.add_edge(category, subcategory)
            for detail, color, description in details:
                G.add_node(detail, color=color, layer="Detail", group=category, description=description)
                G.add_edge(subcategory, detail)
    else:
        for detail, color, description in subcategories:
            G.add_node(detail, color=color, layer="Detail", group=category, description=description)
            G.add_edge(category, detail)

# Create a pyvis network
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Populate the pyvis network with the NetworkX graph
net.from_nx(G)

# Generate the HTML using a Jinja2 template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asherah Network</title>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.css">
    <style>
        body {
            background-color: #222222;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        #network {
            width: 100%;
            height: 750px;
            border: 1px solid lightgray;
        }
        .checkbox-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
        }
        .feedback {
            margin-top: 20px;
        }
        details {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <main class="container">
        <h1>Asherah Network</h1>
        <p>Select the subgraphs you want to display:</p>
        <details open>
            <summary>Toggle Subgraphs</summary>
            <div class="checkbox-group">
                {% for category in categories %}
                    <label><input type="checkbox" value="{{ category }}" onchange="toggleSubgraph(this)" checked> {{ category }}</label>
                {% endfor %}
            </div>
        </details>
        <div id="network"></div>
        <div class="feedback" id="feedback"></div>
        <dialog id="nodeModal">
            <article>
                <header>
                    <button aria-label="Close" rel="prev"></button>
                    <h3 id="modalTitle">Node Title</h3>
                </header>
                <p id="modalDescription">Node Description</p>
            </article>
        </dialog>
    </main>
    <script src="modal.js"></script>
    <script>
        var nodes = new vis.DataSet({{ nodes | tojson }});
        var edges = new vis.DataSet({{ edges | tojson }});

        var container = document.getElementById('network');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {
            nodes: {
                shape: 'dot',
                size: 10,
                font: {
                    size: 14,
                    color: '#ffffff'
                },
                borderWidth: 2
            },
            edges: {
                width: 2,
                color: { inherit: 'from' },
                smooth: { type: 'continuous' }
            },
            interaction: {
                navigationButtons: true,
                keyboard: true
            },
            physics: {
                enabled: true
            }
        };
        var network = new vis.Network(container, data, options);

        network.on("doubleClick", function(params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                showModal(node.label, node.description);
            }
        });

        function showModal(title, description) {
            var modal = document.getElementById('nodeModal');
            document.getElementById('modalTitle').innerText = title;
            document.getElementById('modalDescription').innerText = description;
            openModal(modal);
        }

        document.querySelector('dialog button[aria-label="Close"]').addEventListener('click', function() {
            var modal = document.getElementById('nodeModal');
            closeModal(modal);
        });

        function toggleSubgraph(checkbox) {
            var group = checkbox.value;
            var updateArray = nodes.get({
                filter: function (item) {
                    return item.group === group;
                }
            }).map(function (node) {
                return { id: node.id, hidden: !checkbox.checked };
            });
            nodes.update(updateArray);
            document.getElementById('feedback').innerText = group + ' visibility ' + (checkbox.checked ? 'enabled' : 'disabled') + '.';
        }
    </script>
</body>
</html>
"""

# Prepare nodes and edges for Jinja2
nodes = [
    {"id": node, "label": node, "group": data["group"], "color": data["color"], "description": data.get("description", "")}
    for node, data in G.nodes(data=True)
]
edges = [
    {"from": source, "to": target}
    for source, target in G.edges()
]

# Extract categories for checkboxes
categories = concepts.keys()

template = Template(html_template)
html_output = template.render(nodes=nodes, edges=edges, categories=categories)

# Write the HTML to a file
with open("asherah_network.html", "w") as file:
    file.write(html_output)

print("HTML file generated asherah_network.html")
