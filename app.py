import json
import gradio as gr

# ---------- Case Conversion Functions ----------

def to_snake_case(text):
    return text.lower().replace(" ", "_")

def to_upper_case(text):
    return text.upper().replace(" ", "_")

def to_camel_case(text):
    words = text.split()
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


# ---------- Main JSON Refiner ----------

def refine_json(text, case_type):

    lines = text.split("\n")
    data = {}

    for line in lines:
        if ":" in line:

            key, value = line.split(":",1)

            key = key.strip()
            value = value.strip()

            # ----- Case Conversion -----
            if case_type == "snake_case":
                key = to_snake_case(key)

            elif case_type == "camelCase":
                key = to_camel_case(key)

            elif case_type == "UPPERCASE":
                key = to_upper_case(key)

            # ----- Detect Data Type -----
            if value.isdigit():
                value = int(value)

            elif value.lower() == "true":
                value = True

            elif value.lower() == "false":
                value = False

            else:
                try:
                    value = float(value)
                except:
                    pass

            data[key] = value

    output = json.dumps(data, indent=4)

    stats = f"""
Top-level Keys: {len(data)}
Value Types: {set(type(v).__name__ for v in data.values())}
"""

    return output, stats


# ---------- UI ----------

with gr.Blocks() as demo:

    gr.Markdown("# JSON Refiner")

    with gr.Row():
        inp = gr.Textbox(lines=10, label="Input Key-Value Text")
        out = gr.Code(label="Refined JSON")

    case = gr.Radio(
        ["snake_case","camelCase","UPPERCASE"],
        label="Select Key Case Style",
        value="snake_case"
    )

    stats = gr.Textbox(label="JSON Statistics")

    btn = gr.Button("Refine JSON")

    btn.click(refine_json, inputs=[inp,case], outputs=[out,stats])

demo.launch()
