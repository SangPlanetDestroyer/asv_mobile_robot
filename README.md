Ini merupakan codebase untuk ujian tengah semester dimana membuat gazebo berdasarkan perlombaan asv dengan menggunakan mobile robot.

## World Gazebo

World lapangan tersedia di `worlds/asv_field.world` untuk Gazebo Harmonic
(Gazebo Sim). World ini memiliki ground plane berukuran panjang 60 m dan lebar
30 m. Gambar `images/gambar_lapangan.png` disimpan sebagai referensi tata letak,
tetapi tidak lagi dirender di world. Tanda lingkaran dibuat sebagai 46 bola
static, sedangkan enam tanda persegi panjang dibuat sebagai box static. Semua
objek memiliki collision dan diposisikan mengikuti skala gambar pada bidang.
Di sekeliling dua lapangan terdapat lima segmen tembok coklat: dua segmen
horizontal, dua dinding luar, dan satu dinding tengah yang dipakai bersama.

Jalankan dari root repository setelah environment ROS 2 Jazzy di-source:

```bash
./scripts/run_asv_field.zsh
```

Jika GUI masih kosong setelah percobaan sebelumnya, jalankan kembali dengan
script yang sama:

```bash
./scripts/run_asv_field.zsh
```
