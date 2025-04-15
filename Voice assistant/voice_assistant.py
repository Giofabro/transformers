import gradio as gr
from worker import speech_to_text, text_to_speech, process_message
import os

def handle_input(audio, text):
    user_input = text
    
    # Elabora l'audio se fornito
    if audio is not None:
        audio_path = audio  # Gradio salva l'audio in un file temporaneo
        user_input = speech_to_text(audio_path) or text
    
    if not user_input.strip():
        return "Nessun input ricevuto", "", None
    
    # Processa il messaggio
    response = process_message(user_input)
    
    # Genera l'audio
    audio_path = text_to_speech(response)
    
    # Verifica che il file audio esista
    if audio_path and os.path.exists(audio_path):
        return user_input, response, audio_path
    else:
        return user_input, response, None

with gr.Blocks() as app:
    gr.Markdown("# 🎙️ Assistente Vocale Completo")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="filepath",
                label="Registra Audio"
            )
            text_input = gr.Textbox(
                label="Oppure scrivi qui",
                placeholder="Scrivi il tuo messaggio..."
            )
            submit_btn = gr.Button("Invia", variant="primary")
        
        with gr.Column():
            input_display = gr.Textbox(label="Input riconosciuto", interactive=False)
            output_display = gr.Textbox(label="Risposta", interactive=False)
            audio_output = gr.Audio(
                label="Risposta audio", 
                type="filepath",
                interactive=False
            )

    submit_btn.click(
        handle_input,
        inputs=[audio_input, text_input],
        outputs=[input_display, output_display, audio_output]
    )

if __name__ == "__main__":
    app.launch(server_port=8000, share=True)