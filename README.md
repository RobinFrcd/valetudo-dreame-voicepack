# valetudo-dreame-voicepack

AI Generated voice packs for Valetudo controlled robots.

Tested with Dreame L10s, sound list taken [here](https://github.com/Findus23/voice_pack_dreame/blob/main/sound_list.csv).

## Usage

1. `poetry install` to install
2. `poetry run jupyter lab`
3. Use the `GenerateVoices.ipynb` notebook with our own `VOICE_ID`, `FY_USER` and `FY_PWD`
4. Run the notebook to generate the wav files and `./wav2ogg.sh -i voice_packs/mj/wav -o mj` to generate the tar.gz

You'll need `ffmpeg` and `vorbis-tools` to make the `wav2ogg.sh` script run.

### Available packs
- 🕴🏻Michael Jackson:
    - https://github.com/RobinFrcd/valetudo-dreame-voicepack/releases/download/mj/mj.tar.gz
    - MD5: `d00b935eb75c4284814d4200a4ac940e`

- 👸 QueenElizabethII:
    - https://github.com/RobinFrcd/valetudo-dreame-voicepack/releases/download/QueenElizabethII/Queen_Elizabeth.tar.gz
    - MD5: `af3df2c355a6a2c6aaca00e76b23bbf0`
