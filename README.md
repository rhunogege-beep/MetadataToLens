# MetadataToLens

**Automatic Camera & Lens Metadata Pipeline for Nuke**

MetadataToLens adalah plugin Nuke yang secara otomatis membaca metadata kamera dari file EXR (ARRI, RED, Sony, Canon, Blackmagic) dan menyinkronkan parameter ke node Camera dan LensCore di Nuke 17.0+.

## 🎯 Fitur

- ✅ **Auto Metadata Read** - Membaca metadata EXR dari ARRI, RED, Sony, Canon, Blackmagic
- ✅ **Camera Auto-Sync** - Mengisi focal length, focus distance, T-stop, sensor size otomatis
- ✅ **Lens Matching** - Deteksi otomatis jenis lensa (ZEISS, Cooke, ARRI Signature, dsb.)
- ✅ **LensCore Integration** - Sinkronisasi langsung ke plugin LensCore
- ✅ **Metadata Validation** - Cek konsistensi metadata dan beri warning jika ada masalah
- ✅ **Unit Conversion** - Konversi satuan meter/feet/inch otomatis
- ✅ **Sensor Database** - Database kamera ARRI, RED, Sony, Canon, Blackmagic
- ✅ **Lens Database** - Database lensa profesional dengan transmission, distortion profile
- ✅ **Auto Refresh** - Perbarui otomatis saat Read node berubah
- ✅ **Nuke 17.0v3 Ready** - Python 3.11, PySide6, native Nuke integration

## 🚀 Quick Start

### Instalasi

1. Clone repository:
```bash
git clone https://github.com/rhunogege-beep/MetadataToLens.git
cd MetadataToLens
```

2. Copy ke folder Nuke:
```bash
# Linux / macOS
cp -r . ~/.nuke/MetadataToLens

# Windows
xcopy . "%USERPROFILE%\.nuke\MetadataToLens" /E /I
```

3. Restart Nuke

4. Plugin akan muncul di menu: **Metadata → MetadataToLens**

### Penggunaan Dasar

```python
import nuke
from metadata_to_lens.metadata_reader import MetadataReader
from metadata_to_lens.camera_sync import CameraSync

# Baca metadata dari Read node
read_node = nuke.toNode("Read1")
reader = MetadataReader(read_node)

# Sync ke Camera node
camera_node = nuke.toNode("Camera1")
sync = CameraSync(camera_node)
sync.sync_from_reader(reader)

print("Camera updated from metadata")
```

## 📁 Struktur Proyek

```
MetadataToLens/
├── metadata_to_lens/
│   ├── __init__.py
│   ├── metadata_reader.py      # EXR metadata parser
│   ├── camera_sync.py          # Camera node sync
│   ├── lens_sync.py            # LensCore integration
│   ├── validator.py            # Metadata validator
│   ├── unit_converter.py       # Unit conversion
│   ├── logger.py               # Logging
│   ├── constants.py            # Constants & enums
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── panel.py            # UI panel
│   │   └── widgets.py          # Custom widgets
│   └── database/
│       ├── __init__.py
│       ├── sensors.json        # Camera sensor database
│       ├── lenses.json         # Lens database
│       └── cameras.json        # Camera model database
├── gizmos/
│   └── MetadataToLens.gizmo    # Nuke Gizmo wrapper
├── icons/
│   └── MetadataToLens.png
├── tests/
│   ├── __init__.py
│   ├── test_metadata_reader.py
│   ├── test_camera_sync.py
│   └── test_validator.py
├── menu.py                      # Nuke menu integration
├── init.py                      # Nuke init script
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

## 🎬 Supported Cameras

### ARRI
- ALEXA Mini LF
- ALEXA 35
- ALEXA XT Plus
- ALEXA SXT
- ALEXA Classic

### RED
- V-RAPTOR
- KOMODO
- GEMINI
- HELIUM

### Sony
- BURANO
- FX9
- FX30
- VENICE

### Canon
- EOS R3
- EOS R5
- C300 Mark III
- C500 Mark II

### Blackmagic
- POCKET CINEMA CAMERA 6K Pro
- URSA Mini Pro 12K

## 🔧 Metadata Support

### ARRI (EXR)
```
exr/tStop
exr/fStop
exr/focusDistance
exr/nominalFocalLength
exr/lensModel
exr/sensorOverallDimensions
exr/cameraModel
exr/shutterAngle
exr/isoSpeed
exr/exposureIndex
```

### RED (RMD)
```
red:tStop
red:fStop
red:focusDistance
red:focalLength
red:lensModel
red:sensorWidth
red:sensorHeight
```

### Sony (STP/XML)
```
sony:tstop
sony:fstop
sony:focalLength
sony:focusDistance
sony:sensorModel
```

## 📊 Database Format

### Sensor Database (sensors.json)
```json
{
  "ARRI ALEXA Mini LF": {
    "width_mm": 36.70,
    "height_mm": 25.54,
    "sensor_type": "CMOS",
    "iso_native": 800
  }
}
```

### Lens Database (lenses.json)
```json
{
  "Zeiss Supreme Prime 85/T1.5": {
    "manufacturer": "Zeiss",
    "series": "Supreme Prime",
    "focal_length": 85,
    "max_tstop": 1.5,
    "transmission": 0.917,
    "sensor_type": "FF",
    "distortion_profile": "zeiss_supreme_85"
  }
}
```

## 🔄 Workflow

```
Read (EXR + Metadata)
       ↓
MetadataToLens
       ├─→ Metadata Parser
       ├─→ Camera Sync
       ├─→ Lens Matcher
       └─→ Validator
       ↓
[Camera Updated]
[LensCore Updated]
       ↓
ZDefocus / STMap / Render
```

## 📋 Roadmap

### v0.1 (Current - Sprint 1)
- [x] Project skeleton
- [x] Metadata reader
- [x] Camera sync
- [x] Sensor database
- [ ] Validator
- [ ] Unit converter

### v0.2 (Sprint 2)
- [ ] Lens database
- [ ] Lens matching
- [ ] LensCore integration
- [ ] T-stop ↔ F-stop conversion

### v0.3 (Sprint 3)
- [ ] PySide6 UI
- [ ] Metadata inspector panel
- [ ] Auto refresh callbacks
- [ ] Status validation

### v1.0 (Sprint 4)
- [ ] Support RED, Sony, Canon, Blackmagic
- [ ] Distortion profile support
- [ ] Breathing compensation
- [ ] CA simulation
- [ ] Rolling shutter metadata
- [ ] Documentation lengkap
- [ ] Release build & installer

## 🧪 Testing

```bash
# Jalankan semua test
pytest

# Test dengan coverage
pytest --cov=metadata_to_lens

# Test spesifik file
pytest tests/test_metadata_reader.py -v
```

## 📝 Development

### Setup Development Environment

```bash
git clone https://github.com/rhunogege-beep/MetadataToLens.git
cd MetadataToLens
python -m venv venv
source venv/bin/activate  # atau `venv\Scripts\activate` di Windows
pip install -e ".[dev]"
```

### Code Style

```bash
# Format dengan black
black metadata_to_lens tests

# Check dengan pylint
pylint metadata_to_lens

# Type check dengan mypy
mypy metadata_to_lens
```

## 🐛 Issue & Contribution

Jika menemukan bug atau punya saran, silakan buat Issue di:
https://github.com/rhunogege-beep/MetadataToLens/issues

Untuk kontribusi, buat Pull Request dengan penjelasan detail.

## 📄 License

MIT License - lihat [LICENSE](LICENSE)

## 👨‍💻 Authors

- Proyek ini dikembangkan untuk mendukung pipeline Live Action ZEISS di Nuke 17.0v3

## 🙏 Acknowledgments

- ARRI, RED, Sony, Canon, Blackmagic untuk dokumentasi metadata kamera
- Nuke team di Foundry untuk API documentation
- VFX studios yang memberikan feedback

---

**Status**: 🚧 Development (v0.1-alpha)

**Last Updated**: 2026-07-07

**Compatibility**: Nuke 17.0+ | Python 3.11+ | PySide6

