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

## Robot ROS 2

Model mobile robot hasil migrasi berada di `ros2_ws/src/my_robot`. Model ini
memakai dua roda penggerak, dua caster, IMU, dan kamera yang menghadap ke depan.
Marker AprilTag/ArUco sudah dihapus dari model.

Build dan jalankan simulasi dengan:

```bash
cd ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select my_robot
source install/setup.bash
ros2 launch my_robot asv_gazebo.launch.py
```

Topic kamera yang tersedia adalah `/camera/image_raw` dan
`/camera/camera_info`. Robot menerima perintah gerak melalui `/cmd_vel`.

Jika GUI masih kosong setelah percobaan sebelumnya, jalankan kembali dengan
script yang sama:

```bash
./scripts/run_asv_field.zsh
```
