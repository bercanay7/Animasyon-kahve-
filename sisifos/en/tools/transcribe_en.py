"""English takes -> whisper word timestamps.
Usage: python3 en/tools/transcribe_en.py OUTDIR prompt|noprompt MODEL files...
  MODEL: small | medium.en  (WHISPER_DIR env = download_root, optional)
Writes OUTDIR/<name>.<tag>.words.json  (list of {w,s,e,p})"""
import sys, json, os, whisper, time
outdir, mode, model, files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
m = whisper.load_model(model, download_root=os.environ.get('WHISPER_DIR'))
PROMPT = ('Sisyphus, Thanatos, Aegina, Asopus, Autolycus, Ephyra, Corinth, Merope, Persephone, '
          'Hermes, Tartarus, Camus, Zeus, Ares, Homer.')
tag = model.replace('.', '') + ('' if mode == 'prompt' else '_np')
for path in files:
    t0 = time.time()
    r = m.transcribe(path, language='en', word_timestamps=True, condition_on_previous_text=False,
                     initial_prompt=PROMPT if mode == 'prompt' else None, fp16=False, temperature=0)
    words = [{'w': w['word'].strip(), 's': round(w['start'], 3), 'e': round(w['end'], 3), 'p': round(w.get('probability', 0), 3)}
             for sg in r['segments'] for w in sg['words']]
    name = os.path.basename(path).rsplit('.', 1)[0]
    json.dump(words, open(os.path.join(outdir, f'{name}.{tag}.words.json'), 'w'), ensure_ascii=False)
    print(path, tag, len(words), 'words', round(time.time() - t0, 1), 's', flush=True)
