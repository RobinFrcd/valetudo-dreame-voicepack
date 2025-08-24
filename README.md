# valetudo-dreame-voicepack

AI Generated voice packs for Valetudo controlled robots. Tested with L10S Ultra only.

## Available packs

If you just want to try these on your Valetudo Dreame Robot. Go to `Options - Robot > Misc Options`. Get one of these URLs/MD5 and set the language code to `VA`.

| Voice Pack        | Download URL                                                                | MD5 Hash                             |
|-------------------|-----------------------------------------------------------------------------|--------------------------------------|
| 🕴🏻Michael Jackson | `https://github.com/RobinFrcd/valetudo-dreame-voicepack/releases/download/mj/mj.tar.gz` | `b682f2eadcc51056aff12bea6baf798a`   |
| 👸 QueenElizabethII | `https://github.com/RobinFrcd/valetudo-dreame-voicepack/releases/download/QueenElizabethII/Queen_Elizabeth.tar.gz` | `da81813049ec1feb68fc74e05174f0a9`   |
| 👸2️ QueenElizabethII v2 | `https://github.com/RobinFrcd/valetudo-dreame-voicepack/releases/download/QueenElizabethII-v2/Queen_ElizabethII-v2.tar.gz` | `dbb6bf820e136b17c248453b101914d6`   |

## Usage

If you want to generate new voice

`uv sync` to install

### Generate a new Sound pack

For now, there are two clients [elevenlabs](https://elevenlabs.io/) and [fakeyou](https://fakeyou.com/). Fakeyou is free but a bit bugged.

1. `uv run generate_audio --csv ./sound_list_l10s_ultra.csv --output ./voice_packs/<PACK_NAME> --voice-id <VOICE_ID> --client elevenlabs`
2. `./to_ogg.sh -i ./voice_packs/<PACK_NAME>/mp3 -o <PACK_NAME>`

### Upload files to the robot

Quick and easy way is to start a http server on your machine and pull them from the robot:

1. `python -m http.server`
2. Update [upload_voice.sh](./upload_voice.sh) with the IP of your robot and IP of the http server
3. `./upload_voice.sh -f Queen_Elizabeth.tar.gz`

### Generate sound list
[Sound list](./sound_list.csv) has been extracted with STT from the .ogg files that were in my L10S Ultra.

First recover sound files from the robot:
1. On your PC: `uv run receiver`
2. Connect to your robot (with ssh)
3. (on the robot) Find relevant sound files: `tar -czvf /tmp/robot_sounds.tar.gz -C /audio/ EN/`
4. (on the robot) Recover the files: `curl -T /tmp/robot_sounds.tar.gz http://<LOCAL_SERVER_IP>:8000`

Now you have the files on your PC, you can generate the transcript:
`uv run transcript_generator --input-folder ./robot_sounds/EN --output-csv sound_list_l10s_ultra.csv`

This step uses [elevenlabs](https://elevenlabs.io/) so `ELEVENLABS_API_KEY` is needed in your `.env`
