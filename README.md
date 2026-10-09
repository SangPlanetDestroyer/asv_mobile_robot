# Simulasi Mobile Robot Berbasis Lomba ASV

Ini merupakan codebase untuk ujian tengah semester yang membuat simulasi
Gazebo dari robot mobile dengan aturan misi dan tata letak lapangan yang
terinspirasi dari perlombaan ASV. Tujuan utama proyek ini bukan membuat model
kapal ASV yang memiliki dinamika air, melainkan menguji navigasi otonom,
waypoint, imaging, docking, monitoring, dan fail-safe pada platform mobile
robot di arena yang serupa dengan arena lomba ASV.

Karena platform yang digunakan adalah robot beroda, simulasi ini menggunakan
ground plane dan model diff-drive. Istilah ASV pada nama package, script, dan
controller merujuk pada aturan serta skenario misi yang diadaptasi, bukan pada
representasi fisik kapal atau lingkungan air secara penuh.

Ke depannya, proyek ini juga diarahkan untuk dikembangkan menjadi robot mobile
nyata dan diuji pada lapangan fisik dengan rintangan serta urutan misi yang
serupa dengan arena ASV. Perlombaan ASV menjadi inspirasi utama dalam
merancang misi, tata letak lapangan, objek rintangan, imaging, docking, dan
keselamatan robot.

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

Build dan jalankan simulasi dengan terminal `zsh`:

```zsh
cd ros2_ws
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH COLCON_CURRENT_PREFIX
source /opt/ros/jazzy/setup.zsh
colcon build --packages-select my_robot
source install/setup.zsh
ros2 launch my_robot asv_gazebo.launch.py
```

Atau jalankan semuanya melalui script runner:

```zsh
./scripts/run_asv_robot.zsh
```

Argumen tambahan akan diteruskan ke launch file, misalnya:

```zsh
./scripts/run_asv_robot.zsh --show-args
```

Jika `ros2 launch` menghasilkan error `invalid choice: 'launch'`, pasang ekstensi
launch ROS 2 terlebih dahulu:

```zsh
sudo apt update
sudo apt install ros-jazzy-ros2launch
```

Topic kamera yang tersedia adalah `/camera/image_raw` dan
`/camera/camera_info`. Robot menerima perintah gerak melalui `/cmd_vel`.

Jika GUI masih kosong setelah percobaan sebelumnya, jalankan kembali dengan
script yang sama:

```bash
./scripts/run_asv_field.zsh
```
