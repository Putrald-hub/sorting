#!/usr/bin/env python3
"""
Analisis Performa Algoritma pada Sistem Marketplace / E-Commerce
- Perhitungan nilai inventaris: iteratif vs rekursif
- Sorting harga produk: Selection Sort, Bubble Sort, Insertion Sort
- Dataset CSV: data_produk_100000.csv

Catatan performa:
Algoritma sorting O(n^2) tidak praktis untuk 100.000 data (hingga miliaran perbandingan).
Jalankan benchmark bertahap dengan --sizes 1000,3000,5000, lalu naikkan jika waktu memungkinkan.
Program tetap memuat dataset 100.000 produk untuk kebutuhan dataset tugas.
"""

import argparse
import csv
import random
import statistics
import time
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data_produk_100000.csv")


def load_products(path=DATA_FILE):
    """Membaca data produk dari CSV."""
    products = []
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "id_produk": int(row["id_produk"]),
                "nama_produk": row["nama_produk"],
                "kategori": row["kategori"],
                "harga": int(row["harga"]),
                "stok": int(row["stok"]),
                "rating": float(row["rating"]),
            })
    return products


def total_nilai_iteratif(products):
    """Menghitung total nilai inventaris dengan perulangan."""
    total = 0
    for product in products:
        total += product["harga"] * product["stok"]
    return total


def total_nilai_rekursif(products, index=0):
    """Menghitung total nilai inventaris secara rekursif."""
    # Base case: seluruh produk telah diproses.
    if index >= len(products):
        return 0
    current_value = products[index]["harga"] * products[index]["stok"]
    return current_value + total_nilai_rekursif(products, index + 1)


def selection_sort(items):
    """Selection Sort berdasarkan harga, urutan menaik."""
    arr = items.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j]["harga"] < arr[min_index]["harga"]:
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1
    return arr, comparisons, swaps


def bubble_sort(items):
    """Bubble Sort berdasarkan harga, urutan menaik; berhenti dini jika sudah terurut."""
    arr = items.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j]["harga"] > arr[j + 1]["harga"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return arr, comparisons, swaps


def insertion_sort(items):
    """Insertion Sort berdasarkan harga, urutan menaik."""
    arr = items.copy()
    comparisons = 0
    shifts = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j]["harga"] > key["harga"]:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comparisons, shifts


SORTS = {
    "Selection Sort": selection_sort,
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
}


def benchmark(products, sizes, repeats=1):
    """Benchmark sorting pada potongan data yang sama untuk setiap algoritma."""
    print("\n=== BENCHMARK SORTING HARGA PRODUK ===")
    print(f"{'Ukuran':>8} | {'Algoritma':<17} | {'Waktu (detik)':>14} | {'Perbandingan':>14} | {'Swap/Shift':>12} | Valid")
    print("-" * 91)
    for size in sizes:
        if size > len(products):
            print(f"Ukuran {size} dilewati: dataset hanya berisi {len(products)} data.")
            continue
        sample = products[:size]
        for name, algorithm in SORTS.items():
            durations = []
            final_result = None
            comparisons = operations = 0
            for _ in range(repeats):
                start = time.perf_counter()
                final_result, comparisons, operations = algorithm(sample)
                durations.append(time.perf_counter() - start)
            elapsed = statistics.median(durations)
            valid = all(final_result[i]["harga"] <= final_result[i + 1]["harga"]
                        for i in range(len(final_result) - 1))
            print(f"{size:>8} | {name:<17} | {elapsed:>14.4f} | {comparisons:>14,} | {operations:>12,} | {'Ya' if valid else 'Tidak'}")


def main():
    parser = argparse.ArgumentParser(description="Analisis algoritma untuk data marketplace.")
    parser.add_argument("--data", default=str(DATA_FILE), help="Lokasi file CSV dataset.")
    parser.add_argument("--sizes", default="1000,3000,5000",
                        help="Ukuran sampel benchmark, pisahkan dengan koma. Contoh: 25000,50000,75000,100000")
    parser.add_argument("--repeats", type=int, default=1, help="Jumlah pengulangan benchmark (median dilaporkan).")
    parser.add_argument("--recursive-demo", type=int, default=500,
                        help="Jumlah produk awal untuk demo rekursif agar tidak melewati batas rekursi Python.")
    args = parser.parse_args()

    products = load_products(args.data)
    print("ANALISIS PERFORMA ALGORITMA MARKETPLACE / E-COMMERCE")
    print("=" * 58)
    print(f"Jumlah produk dalam dataset : {len(products):,}")
    print("Contoh 5 produk:")
    for product in products[:5]:
        print(f"  ID {product['id_produk']:>6} | {product['nama_produk']:<24} | Rp{product['harga']:>9,} | stok {product['stok']}")

    print("\n=== ITERATIF VS REKURSIF: TOTAL NILAI INVENTARIS ===")
    # Gunakan subset yang SAMA agar perbandingan waktu iteratif vs rekursif adil.
    recursive_data = products[:min(args.recursive_demo, len(products))]

    iterative_start = time.perf_counter()
    iterative_total = total_nilai_iteratif(recursive_data)
    iterative_time = time.perf_counter() - iterative_start

    recursive_start = time.perf_counter()
    recursive_total = total_nilai_rekursif(recursive_data)
    recursive_time = time.perf_counter() - recursive_start

    print(f"Jumlah data untuk kedua fungsi: {len(recursive_data):,} produk")
    print(f"Iteratif ({len(recursive_data):,} produk): Rp{iterative_total:,} | {iterative_time:.6f} detik")
    print(f"Rekursif ({len(recursive_data):,} produk): Rp{recursive_total:,} | {recursive_time:.6f} detik")
    print(f"Validasi hasil kedua fungsi: {'SAMA' if recursive_total == iterative_total else 'BERBEDA'}")
    print("Kompleksitas iteratif: O(n) waktu, O(1) ruang tambahan.")
    print("Kompleksitas rekursif: O(n) waktu, O(n) ruang stack.")

    sizes = [int(x.strip()) for x in args.sizes.split(",") if x.strip()]
    if any(size < 1 for size in sizes):
        parser.error("Ukuran benchmark harus lebih besar dari 0.")
    if any(size >= 25000 for size in sizes):
        print("\\nPERINGATAN: ukuran benchmark >= 25.000 dengan algoritma O(n^2) dapat memerlukan waktu sangat lama.")
        print("Selection/Bubble/Insertion Sort pada 100.000 data dapat membutuhkan miliaran operasi.")
        print("Program tetap melanjutkan karena ukuran tersebut diminta secara eksplisit. Hentikan dengan Ctrl+C jika terlalu lama.\\n")
    benchmark(products, sizes, max(1, args.repeats))


if __name__ == "__main__":
    main()
