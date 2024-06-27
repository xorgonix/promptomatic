from pyvis.network import Network
import networkx as nx

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
    G.add_node(category, color="#0000FF", layer="Category")
    if isinstance(subcategories, dict):
        for subcategory, details in subcategories.items():
            G.add_node(subcategory, color="#00FF00", layer="Subcategory")
            G.add_edge(category, subcategory)
            for detail, color in details:
                G.add_node(detail, color=color, layer="Detail")
                G.add_edge(subcategory, detail)
    else:
        for detail, color in subcategories:
            G.add_node(detail, color=color, layer="Detail")
            G.add_edge(category, detail)

# Create a pyvis network
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", filter_menu=True, select_menu=True)

# Populate the pyvis network with the NetworkX graph
net.from_nx(G)

# Add physics settings buttons
net.show_buttons(filter_=['physics'])

# Generate the network and open in the browser
net.show("asherah_network.html", notebook=False)
