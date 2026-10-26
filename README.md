<video src="demo/DemoPCVproject.webm" controls width="100%"></video>

# 🏀 Catch WOWO Ball

**Catch WOWO Ball** adalah sebuah proyek game interaktif berbasis *Computer Vision* yang memadukan grafik 2D dan pemrosesan video secara *real-time*. Game ini dirancang untuk memberikan pengalaman bermain yang unik, di mana pemain dapat mengontrol objek di dalam game menggunakan benda nyata di dunia fisik tanpa perlu menyentuh keyboard atau mouse saat bermain.

---

## 📚 Library yang Dipakai

Proyek ini dibangun menggunakan beberapa library utama Python:

* **Pygame**: Digunakan untuk mengelola antarmuka game (UI), *rendering* grafik 2D, mendeteksi input mouse/keyboard, serta mengatur alur *game loop* dan FPS.
* **OpenCV (`cv2`)**: Digunakan untuk mengakses webcam, mengolah *frame* video secara *real-time*, melakukan segmentasi warna, serta melacak koordinat posisi benda.
* **NumPy**: Digunakan untuk manipulasi matriks gambar dan pemrosesan data array dari *frame* video OpenCV.

---

## 📁 Penjelasan Setiap Direktori

Berikut adalah struktur folder dalam proyek beserta fungsinya masing-masing:

* **`ball/`**: Berisi kelas dan logika untuk objek bola (`Ball`). Mengatur posisi awal, kecepatan jatuh bola, reset posisi saat bola keluar/tertangkap, serta fungsi *rendering* bola ke layar.
* **`basket/`**: Berisi kelas dan logika untuk keranjang (`Basket`). Mengatur ukuran, warna, posisi batas layar, serta pembaruan posisi horizontal berdasarkan masukan dari pelacak (*tracker*).
* **`controller/`**: Berisi kontroler utama game (`MainGame`). Mengatur alur logika game, status alur (Menu/Play), penanganan tombol UI, pemrosesan event keyboard/mouse, serta skor.
* **`tracker/`**: Berisi pustaka pelacak (*Tracker*). Bertanggung jawab membaca *frame* dari webcam, mengubah skema warna ke HSV, mendeteksi area benda hitam, dan mengembalikan rasio posisi sumbu X.
* **`demo/`**: Berisi berkas media pendukung berupa rekaman video singkat (*Demo PCV project.webm*) yang menampilkan cara kerja dan *gameplay* dari proyek ini.

---

## 🎮 Cara Bermain

1. **Persiapan**: Pastikan webcam pada komputer/laptop Anda sudah aktif dan berfungsi dengan baik.
2. **Navigasi Menu**: Jalankan program, lalu klik tombol **PLAY** pada menu utama menggunakan kursor mouse.
3. **Kontrol Keranjang**:
   * Ambil benda apa saja yang berwarna **HITAM** (misalnya spidol, ponsel, atau benda hitam lainnya).
   * Arahkan benda hitam tersebut ke depan kamera/webcam.
   * **Keranjang akan bergerak mengikuti posisi horizontal (kiri–kanan) dari benda berwarna hitam tersebut secara *real-time*.**
4. **Tujuan Game**:
   * Gerakkan keranjang ke kiri dan ke kanan untuk menangkap bola yang jatuh dari atas.
   * Setiap kali bola berhasil ditangkap, skor Anda akan bertambah **+1**.
   * Jika bola lepas dan jatuh melewati batas bawah layar, skor Anda akan berkurang **-1**.
5. **Kembali ke Menu**: Tekan tombol **ESC** pada keyboard untuk pause atau kembali ke menu utama.