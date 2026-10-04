Ini merupakan codebase untuk ujian tengah semester dimana membuat gazebo berdasarkan perlombaan asv dengan menggunakan mobile robot.

## World Gazebo

World lapangan tersedia di `worlds/asv_field.world` untuk Gazebo Harmonic
(Gazebo Sim). World ini memiliki ground plane berukuran panjang 60 m dan lebar
30 m, dengan gambar `images/gambar_lapangan.png` dirender di atasnya.

Jalankan dari root repository setelah environment ROS 2 Jazzy di-source:

```bash
./scripts/run_asv_field.zsh
```

Jika GUI masih kosong setelah percobaan sebelumnya, jalankan kembali dengan
script yang sama:

```bash
./scripts/run_asv_field.zsh
```
