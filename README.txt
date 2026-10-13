ANALISIS PERFORMA ALGORITMA PADA SISTEM MARKETPLACE / E-COMMERCE
==================================================================

ISI FOLDER
----------
1. main_marketplace.py      : program utama
2. data_produk_100000.csv   : dataset simulasi 100.000 produk
3. README.txt               : petunjuk menjalankan program

FITUR
-----
- Membaca katalog produk dari CSV.
- Menghitung total nilai inventaris (harga x stok) dengan metode iteratif.
- Menghitung total nilai inventaris dengan metode rekursif pada subset aman.
- Membandingkan Selection Sort, Bubble Sort, dan Insertion Sort berdasarkan:
  waktu eksekusi, jumlah perbandingan, jumlah swap/shift, dan validitas hasil.
- Dataset berisi 100.000 produk simulasi, bukan data transaksi nyata.

CARA MENJALANKAN
----------------
Pastikan Python 3 sudah terpasang. Tidak memerlukan library eksternal.

Windows:
  python main_marketplace.py

macOS/Linux:
  python3 main_marketplace.py

Benchmark bertahap per kelipatan 25.000 sampai 100.000:
  python main_marketplace.py --sizes 25000,50000,75000,100000

Benchmark percobaan yang lebih ringan:
  python main_marketplace.py --sizes 1000,3000,5000
  python main_marketplace.py --sizes 1000,3000,5000,10000

Mengatur jumlah pengulangan:
  python main_marketplace.py --sizes 1000,3000 --repeats 3

Mengatur jumlah produk untuk demo rekursif:
  python main_marketplace.py --recursive-demo 500

CATATAN PENTING TENTANG 100.000 DATA
------------------------------------
Dataset yang disediakan berisi 100.000 produk. Namun, Selection Sort, Bubble Sort,
dan Insertion Sort rata-rata membutuhkan waktu O(n^2). Pada 100.000 data,
jumlah perbandingan bisa mendekati 5.000.000.000 untuk satu algoritma.
Karena itu, program secara default melakukan benchmark bertahap pada sampel
1.000, 3.000, dan 5.000 data agar komputer tidak langsung macet. Jika memang ingin
menguji kelipatan 25.000 hingga 100.000, jalankan perintah yang dicantumkan di atas.
Program akan menampilkan peringatan terlebih dahulu di output, tetapi tetap melanjutkan.

Jangan menuliskan waktu hasil perkiraan sebagai hasil eksperimen. Catat waktu
yang benar-benar dihasilkan komputer. Jika instruksi dosen mewajibkan setiap
algoritma benar-benar dijalankan pada 100.000 elemen, diskusikan kelayakan
waktu pengujian dengan dosen atau gunakan lingkungan/implementasi yang sesuai.

RINGKASAN KOMPLEKSITAS
----------------------
Algoritma        | Best case       | Average case | Worst case | Ruang tambahan
Selection Sort   | O(n^2)          | O(n^2)       | O(n^2)     | O(1)
Bubble Sort      | O(n)*           | O(n^2)       | O(n^2)     | O(1)
Insertion Sort   | O(n)*           | O(n^2)       | O(n^2)     | O(1)

* Bubble Sort pada implementasi ini memakai penghentian dini jika sudah terurut.
  Insertion Sort best case terjadi saat data sudah terurut.

CATATAN ITERATIF VS REKURSIF
----------------------------
Kedua pendekatan menghitung masalah yang sama, yaitu jumlah harga x stok,
serta menggunakan subset data yang SAMA (default 500 produk) agar perbandingan
waktu adil. Ubah jumlahnya dengan --recursive-demo jika diperlukan.
Iteratif memiliki O(1) ruang tambahan; rekursif memiliki O(n) ruang stack.
Python memiliki batas kedalaman rekursi, sehingga demo rekursif dibatasi ke
subset data yang relatif kecil. Waktu kedua fungsi diukur secara terpisah.

SARAN ISI LAPORAN / VIDEO
-------------------------
1. Jelaskan konteks katalog produk marketplace.
2. Demo data produk dan perhitungan inventaris iteratif/rekursif.
3. Jelaskan cara kerja ketiga algoritma sorting.
4. Tampilkan tabel hasil benchmark yang benar-benar dijalankan.
5. Bandingkan waktu, perbandingan, swap/shift, dan kompleksitas.
6. Simpulkan algoritma yang paling sesuai berdasarkan hasil uji, bukan asumsi.
