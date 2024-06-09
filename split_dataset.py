import os
import shutil
import random
import csv

# Path dataset yang akan dibagi
dataset_paths = {
    'aeromonas': 'LibraryDataset/Training/Aeromonas',
    'penyakit_lain': 'LibraryDataset/Training/Penyakit_Lain/',
    'sehat': 'LibraryDataset/Training/Sehat'
}

# Path untuk menyimpan dataset yang sudah dibagi
manual_dataset_paths = {
    'training': 'ManualDataset/Training',
    'testing': 'ManualDataset/Testing'
}

# Fungsi untuk membagi dataset
def split_dataset(source_dir, train_dir, test_dir, split_ratio):
    # Membuat direktori training dan testing jika belum ada
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # Inisialisasi list untuk menyimpan data label
    testing_labels = []
    
    # Iterasi melalui setiap kategori dataset
    for category, path in source_dir.items():
        # Membuat direktori di dalam direktori training untuk setiap kategori
        train_category_dir = os.path.join(train_dir, category)
        os.makedirs(train_category_dir, exist_ok=True)
        
        # Mendapatkan daftar file dalam setiap kategori
        files = os.listdir(path)
        # Mengacak urutan file
        random.shuffle(files)
        # Menghitung jumlah file untuk training
        train_size = int(len(files) * split_ratio)
        
        # Memindahkan file ke direktori training
        for file in files[:train_size]:
            src = os.path.join(path, file)
            dst = os.path.join(train_category_dir, file)
            shutil.copy(src, dst)
        
        # Memindahkan file ke direktori testing dan menyimpan labelnya
        for file in files[train_size:]:
            src = os.path.join(path, file)
            dst = os.path.join(test_dir, file)
            shutil.copy(src, dst)
            testing_labels.append((file, category))
    
    # Menyimpan label testing ke dalam file CSV
    csv_path = os.path.join(test_dir, 'testing_labels.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'true_label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for filename, true_label in testing_labels:
            writer.writerow({'filename': filename, 'true_label': true_label})

    print(f"File CSV berhasil dibuat di: {csv_path}")

# Proses pemisahan dataset dengan rasio 60% training dan 40% testing
split_ratio = 0.6
split_dataset(dataset_paths, manual_dataset_paths['training'], manual_dataset_paths['testing'], split_ratio)

print("Pemisahan dataset selesai.")
