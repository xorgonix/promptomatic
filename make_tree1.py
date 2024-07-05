import re
import json

def parse_markdown(markdown_text):
    lines = markdown_text.split('\n')
    root = {
        "title": "root",
        "level": 0,
        "content": "",
        "leaf": False,
        "children": []
    }
    stack = [root]

    def create_node(level, title):
        return {
            "title": title,
            "level": level,
            "content": "",
            "leaf": True,
            "children": []
        }

    for line in lines:
        heading_match = re.match(r'^(#+) (.+)', line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            current_node = create_node(level, title)

            while stack and stack[-1]['level'] >= level:
                stack.pop()

            stack[-1]['children'].append(current_node)
            stack[-1]['leaf'] = False
            stack.append(current_node)
        else:
            if stack:
                stack[-1]['content'] += line.strip() + '\n'

    return root['children']

def markdown_to_json(markdown_text):
    json_structure = parse_markdown(markdown_text)
    return json.dumps(json_structure, indent=2)

# Example Markdown document
markdown_text = """# Report: Asherah - The Goddess and Her Legacy

## Introduction
The discovery of the Ugaritic texts in 1929 significantly altered our understanding of ancient Near Eastern religions, revealing the presence and importance of the goddess Asherah. Contrary to prior historical and biblical scholarship, Asherah was not only a major deity in the Canaanite pantheon but also held a significant place in ancient Israelite religion. This report delves into the historical, archaeological, and textual evidence of Asherah's worship and her enduring legacy in the religious practices of ancient Israel and Judah.

## Asherah in Ancient Cultures
### Mesopotamian Origins
- Asherah, known as Ashru or Ashum in Mesopotamia, was the consort of the god Amuru.
- Highly venerated during the first Babylonian Dynasty, she had her own temple and priests.
- Her Amorite origins are highlighted by her epithet "Lady of the Steppe" and her association with the mountains.

### Spread and Influence
- Asherah was worshipped across the Hittite Empire, Syria, Mesopotamia, and Southwestern Arabia.
- In Ugarit, she was known as Athirat, the consort of the supreme god El, and bore the title "Creatrix of the Gods."

## Asherah in Canaanite and Israelite Religion
### Integration into Israelite Worship
- Archaeological and textual evidence indicates that Asherah was worshipped in Israel, often alongside Yahweh.
- Symbols of Asherah, such as stylized trees or poles (asherim), were present in the Jerusalem Temple.
- Asherah's iconography often included fertility symbols, such as the Tree of Life, and she was depicted as nourishing and blessing.

### Biblical References and Changes
- The Old Testament contains numerous indirect references to Asherah, often as cultic objects associated with her worship.
- Reformist narratives, such as those of Kings Asa and Josiah, describe efforts to remove Asherah worship from Israelite religion, though these accounts often reflect later theological biases.

## Key Points and Implications
### Historical Significance
- The Ugaritic texts provided irrefutable evidence of Asherah's role in ancient Near Eastern religion and her connection to the Israelite god El.
- Asherah's worship persisted in Israel despite efforts by later reformist movements to suppress her cult.

### Religious Integration
- Asherah's symbols and possibly even her worship were integrated into Israelite religious practices, suggesting a syncretic blending of Canaanite and Israelite beliefs.
- The persistence of Asherah-related symbols, such as the almond tree motif, indicates her enduring influence even after the official establishment of Yahwism.

### Risks and Opportunities
#### Risks
- Misinterpretation of historical and religious texts can lead to biased or incomplete understandings of ancient religious practices.
- Potential backlash from religious communities that may resist reinterpretations of traditional narratives.

#### Opportunities
- Greater understanding of ancient Near Eastern religions can provide richer insights into the historical development of monotheistic traditions.
- Archaeological discoveries continue to offer new perspectives on the interconnectedness of ancient cultures and their religious practices.

## Conclusion
Asherah's presence in ancient Israelite religion challenges traditional narratives of strict monotheism and reveals a more complex religious landscape. The enduring symbols associated with Asherah highlight her significant role in the cultural and religious life of ancient Israel and provide a deeper understanding of the development of early religious beliefs.

---

## Talking Points for a Cocktail Party

1. **Introduction to Asherah**:
   - "Did you know that recent archaeological findings have revealed that the ancient Israelites worshipped a goddess named Asherah alongside Yahweh?"

2. **Significance of Ugaritic Texts**:
   - "The discovery of the Ugaritic texts in 1929 provided concrete evidence of Asherah's role in the ancient Near Eastern pantheon and her connection to the Israelite god El."

3. **Integration into Israelite Religion**:
   - "Asherah was not only a Canaanite goddess but also deeply integrated into Israelite worship, often symbolized by the Tree of Life and other fertility symbols."

4. **Biblical References**:
   - "The Old Testament contains numerous references to cultic objects associated with Asherah, reflecting her once prominent role in Israelite religion."

5. **Reformist Movements**:
   - "Historical reformist movements in ancient Israel, such as those by Kings Asa and Josiah, sought to suppress Asherah worship, though these accounts often reflect later theological biases."

6. **Enduring Symbols**:
   - "Symbols related to Asherah, like the almond tree, persisted in Israelite culture and were even integrated into the symbolism of the Jerusalem Temple."

7. **Modern Implications**:
   - "Understanding the role of Asherah in ancient Israelite religion can provide richer insights into the historical development of monotheistic traditions and the complex interplay of ancient religious beliefs."
"""

# Convert markdown to JSON
json_output = markdown_to_json(markdown_text)
print(json_output)
