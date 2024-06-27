from pyvis.network import Network
import networkx as nx
from jinja2 import Template

# Initialize the graph
G = nx.DiGraph()

# Concepts with descriptions and colors
concepts = {
    "Ancient Cultures": {
        "Mesopotamian Origins": [
            ("Known as Ashru or Ashum", "#FF5733"),
            ("Consort of Amuru", "#FF5733"),
            ("Highly venerated during the first Babylonian Dynasty", "#FF5733"),
            ("Had her own temple and priests", "#FF5733"),
            ("Amorite origins highlighted by her epithet 'Lady of the Steppe'", "#FF5733"),
            ("Associated with mountains", "#FF5733")
        ],
        "Spread and Influence": [
            ("Worshipped across Hittite Empire, Syria, Mesopotamia, Southwestern Arabia", "#FF5733"),
            ("Known as Athirat in Ugarit", "#FF5733"),
            ("Consort of supreme god El", "#FF5733"),
            ("Bore title 'Creatrix of the Gods'", "#FF5733")
        ]
    },
    "Canaanite and Israelite Religion": {
        "Integration into Israelite Worship": [
            ("Archaeological and textual evidence", "#33FF57"),
            ("Symbols such as stylized trees or poles (asherim)", "#33FF57"),
            ("Present in Jerusalem Temple", "#33FF57"),
            ("Iconography included fertility symbols", "#33FF57"),
            ("Depicted as nourishing and blessing", "#33FF57")
        ],
        "Biblical References and Changes": [
            ("Old Testament indirect references", "#33FF57"),
            ("Cultic objects associated with her worship", "#33FF57"),
            ("Reformist narratives by Kings Asa and Josiah", "#33FF57"),
            ("Efforts to remove Asherah worship", "#33FF57"),
            ("Reflects later theological biases", "#33FF57")
        ]
    },
    "Key Points and Implications": {
        "Historical Significance": [
            ("Ugaritic texts evidence of Asherah's role", "#3357FF"),
            ("Connection to the Israelite god El", "#3357FF"),
            ("Persistent worship despite reformist efforts", "#3357FF")
        ],
        "Religious Integration": [
            ("Symbols integrated into Israelite practices", "#3357FF"),
            ("Syncretic blending of beliefs", "#3357FF"),
            ("Enduring influence of symbols like almond tree", "#3357FF")
        ],
        "Risks": [
            ("Misinterpretation of historical texts", "#FF33A6"),
            ("Potential backlash from religious communities", "#FF33A6")
        ],
        "Opportunities": [
            ("Richer insights into monotheistic traditions", "#FF33A6"),
            ("New perspectives from archaeological discoveries", "#FF33A6")
        ]
    },
    "Conclusion": [
        ("Challenges traditional narratives of strict monotheism", "#FF5733"),
        ("Reveals complex religious landscape", "#FF5733"),
        ("Enduring symbols highlight her significant role", "#FF5733"),
        ("Provides deeper understanding of early religious beliefs", "#FF5733")
    ],
    "Talking Points for a Cocktail Party": [
        ("Introduction to Asherah", "#33FF57"),
        ("Significance of Ugaritic Texts", "#33FF57"),
        ("Integration into Israelite Religion", "#33FF57"),
        ("Biblical References", "#33FF57"),
        ("Reformist Movements", "#33FF57"),
        ("Enduring Symbols", "#33FF57"),
        ("Modern Implications", "#33FF57")
    ]
}

# Add nodes and edges to the graph
for category, subcategories in concepts.items():
    G.add_node(category, color="#0000FF", layer="Category", group=category)
    if isinstance(subcategories, dict):
        for subcategory, details in subcategories.items():
            G.add_node(subcategory, color="#00FF00", layer="Subcategory", group=category)
            G.add_edge(category, subcategory)
            for detail, color in details:
                G.add_node(detail, color=color, layer="Detail", group=category)
                G.add_edge(subcategory, detail)
    else:
        for detail, color in subcategories:
            G.add_node(detail, color=color, layer="Detail", group=category)
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
    </style>
</head>
<body>
    <main class="container">
        <h1>Asherah Network</h1>
        <p>Select the subgraphs you want to display:</p>
        <div class="checkbox-group">
            <label><input type="checkbox" value="Ancient Cultures" onchange="toggleSubgraph(this)"> Ancient Cultures</label>
            <label><input type="checkbox" value="Canaanite and Israelite Religion" onchange="toggleSubgraph(this)"> Canaanite and Israelite Religion</label>
            <label><input type="checkbox" value="Key Points and Implications" onchange="toggleSubgraph(this)"> Key Points and Implications</label>
            <label><input type="checkbox" value="Conclusion" onchange="toggleSubgraph(this)"> Conclusion</label>
            <label><input type="checkbox" value="Talking Points for a Cocktail Party" onchange="toggleSubgraph(this)"> Cocktail Party Points</label>
        </div>
        <div id="network"></div>
        <div class="feedback" id="feedback"></div>
    </main>
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
    {"id": node, "label": node, "group": data["group"], "color": data["color"]}
    for node, data in G.nodes(data=True)
]
edges = [
    {"from": source, "to": target}
    for source, target in G.edges()
]

template = Template(html_template)
html_output = template.render(nodes=nodes, edges=edges)

# Write the HTML to a file
with open("asherah_network.html", "w") as file:
    file.write(html_output)

print("HTML file generated asherah_network.html")
