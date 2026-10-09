# Referensi Lomba ASV KKI 2026

Dokumen ini merangkum informasi sub-kategori **Autonomous Surface Vessel
(ASV)** dari `materi-pembelajaran/Panduan-KKI-2026_Final_1-1.PDF`.

## Gambaran Umum

- ASV merupakan sub-kategori Kontes Kapal Indonesia (KKI) 2026.
- Peserta merancang, membuat, dan mendemonstrasikan prototipe kapal coast
  guard otonom berskala model.
- Lomba dilaksanakan di Waduk PDAM Kota Bengkalis.
- Prototipe harus mampu bernavigasi mandiri dan menampilkan monitoring daring
  secara real-time.
- Prototipe yang pernah digunakan dalam kontes lain tidak dapat diikutsertakan
  kembali pada KKI 2026.

## Misi Lomba

Misi dilaksanakan secara berurutan:

1. Berangkat dari starting dock yang ditentukan.
2. Menavigasi 10 pasang bola apung merah-hijau, atau 20 bola, dengan jarak
   antar pasangan 2 meter.
3. Mengambil gambar/video permukaan air pada area kotak hijau sebagai
   simulasi surface surveillance.
4. Mengambil gambar/video bawah permukaan air pada area kotak biru sebagai
   simulasi underwater surveillance.
5. Mengirim hasil imaging ke dashboard web secara real-time.
6. Melakukan docking secara akurat di dermaga finish dan menyentuh bola
   docking biru.

## Ketentuan Prototipe

- Prototipe harus sepenuhnya otonom. Keputusan navigasi diambil oleh sistem
  onboard dan tidak boleh dikendalikan manual selama misi.
- Wajib memiliki sistem propulsi mandiri, kendali otonom, sensor, dan
  komunikasi.
- Ukuran minimum: panjang 60 cm dan lebar 20 cm.
- Berat minimum: 7 kg, termasuk baterai dan periferal.
- Monitoring posisi, heading, dan kecepatan wajib ditampilkan melalui web
  secara real-time serta dapat diakses panitia dan peserta lain.
- Sistem redundan dan subsistem pendukung diizinkan, termasuk grid meshing,
  UAV pendamping, atau kapal tambahan untuk monitoring.

### Referensi Warna Arena

- Bola lintasan: merah dan hijau.
- Kotak misi: hijau untuk surface imaging dan biru untuk underwater imaging.
- Bola docking: biru.
- Acuan warna cat Pylox: merah 115 (PB115), hijau 110 (PB110), dan biru 107
  (PB107).
- Docking menggunakan 3 bola biru dengan jarak antar titik tengah 30 cm.
- Nilai docking dihitung dari jumlah bola biru yang pertama kali disentuh oleh
  bagian kapal saat docking.

## Sistem Kontes dan Lintasan

Sebelum run dimulai, sistem monitoring web harus aktif dan dapat diakses secara
online. Kapal kemudian start dari dermaga, mengikuti jalur 10 pasang bola
merah-hijau, melakukan surface imaging pada kotak hijau, underwater imaging
pada kotak biru, lalu docking di dermaga finish.

Lintasan, posisi dermaga, dan layout venue akan dijelaskan lebih rinci dalam
Petunjuk Teknis ASV KKI 2026 yang diterbitkan terpisah oleh panitia.

## Penilaian Performa

| Komponen      | Simbol       | Ketentuan                                                                                                       |
| ------------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| Kecepatan     | `NT`         | Waktu tempuh lintasan penuh dalam detik. Waktu lebih kecil mendapat nilai lebih besar.                          |
| Misi          | `NM`         | Maksimal 20 poin untuk navigasi lintasan, imaging, dan docking yang berhasil.                                   |
| Penalti       | `P`          | -5 poin setiap pelanggaran. Jika pelanggaran lebih dari 5 kali, run diulang dari START.                         |
| Image quality | `IMH`, `IMB` | Nilai masing-masing imaging: 0, 1, 3, atau 5 berdasarkan keberadaan gambar, bentuk kotak, dan kesesuaian warna. |
| Docking       | `DC`         | Nilai 0, 5, 10, atau 15 berdasarkan jumlah bola docking yang disentuh.                                          |

Pelanggaran meliputi menyentuh bola/buoy, kapal/objek lain, kotak misi, atau
docking di dermaga yang salah.

Formula nilai performa:

```text
Jika NM = 20:
Total = 100 x ((2 x NM - P) / NT) + IM + DC

Jika NM < 20:
Total = 10 x ((2 x NM - P) / 900)

IM = IMH + IMB
DC = 5 x jumlah bola biru yang disentuh saat pertama kali menyentuh dock
```

Pemenang ditentukan berdasarkan total nilai tertinggi: Juara 1, Juara 2,
Juara 3, Harapan 1, dan Harapan 2. Jika terjadi nilai sama, peringkat
ditentukan berdasarkan waktu tempuh tercepat.

## Waktu dan Pengumpulan Video

- Durasi maksimal setiap run adalah 20 menit, termasuk 5 menit setup dan 5
  menit clearing area.
- Video run wajib diunggah ke portal resmi KKI 2026 dan YouTube paling lambat
  H-1 sebelum hari final.

## Penilaian Proposal

Nilai proposal memiliki bobot 40% dari Nilai Akhir. Skor setiap indikator adalah
1 sampai 5, dengan 1 = buruk dan 5 = sangat baik. Nilai dihitung dari bobot
dikalikan skor.

Komponen proposal berbobot:

- Halaman sampul dan lembar pengesahan: wajib.
- Pendahuluan, tujuan, dan misi kapal coast guard: 5%.
- Desain teknis dan spesifikasi:
  - Operational requirement dan ukuran utama: 10%.
  - General arrangement: 10%.
  - Lines plan: 10%.
  - Perkiraan daya/power propulsi: 10%.
  - Tahapan pengerjaan dan metode fabrikasi: 10%.
  - Sensor, instrumentasi, dan display monitoring real-time: 10%.
  - Telekomunikasi dan jaringan: 7%.
  - Back-end development: 7%.
  - Front-end dashboard web real-time: 7%.
  - Peralatan penggerak: 6%.
- Rancangan biaya dan jadwal: masing-masing 5%.
- Penutup: 5%.
- Daftar pustaka: 5%.
- Biodata anggota tim dan job-desk: 5%.

## Penilaian Laporan Kemajuan

Peserta yang lolos proposal wajib membuat prototipe sesuai proposal dan
mengunggah video kemajuan. Masing-masing indikator berikut berbobot 10%:

1. Perkenalan anggota dan job-desk.
2. Uraian misi kapal coast guard dalam skala penuh.
3. Pembuatan lambung prototipe.
4. Pemasangan kemudi dan sistem kendali.
5. Pemasangan sistem propulsi/permesinan.
6. Pengukuran dan verifikasi berat prototipe.
7. Uji propulsi, kemudi, sensor, dan monitoring.
8. Uji gerak lurus dan zigzag.
9. Uji gerak turning atau belok.
10. Uji prototipe sesuai misi dan alur lintasan sebenarnya.

## Keselamatan Wajib

- Emergency stop onboard harus dapat mematikan sistem propulsi dan kendali
  dari jarak jauh serta didemonstrasikan saat inspeksi teknis.
- Sistem wajib memiliki geofence atau batas zona kerja otonom.
- Jika kehilangan sinyal komunikasi atau mengalami kegagalan navigasi, ASV
  harus berhenti otomatis di posisinya dalam fail-safe mode.
- Propeller wajib memakai pelindung berupa cage atau shroud.
- Monitoring real-time harus aktif sebelum run. Panitia berwenang menghentikan
  run jika koneksi terputus.
- ASV tanpa fail-safe tidak lulus Technical Safety Inspection (TSI) dan tidak
  diizinkan bertanding.

## Sumber

Panduan Kontes Kapal Indonesia 2026, Dit. Belmawa, sub-bab 4.4 dan ketentuan
keselamatan pada bab 5.
