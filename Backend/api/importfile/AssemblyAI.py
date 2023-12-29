import assemblyai as aai

class VoiceToText():
        search ="Hello."
        aai.settings.api_key = "147cacab598c4c77b5cb4bb2d3ae295c"
        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe("C:\\Users\\user\\Desktop\\hello.m4a")
        # transcript = transcriber.transcribe("./my-local-audio-file.wav")

        print(transcript.text)

        if search == transcript.text:
            print("yes")
        else:
            print("No")


